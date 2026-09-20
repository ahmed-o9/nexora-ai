from __future__ import annotations

from typing import Any, Dict, List

import httpx

from ..core.config import get_settings


class GoogleImageSearchTool:
    """
    Google Programmable Search image-search tool.

    Configuration comes from the central Nexora settings.

    Required when enabled:
        GOOGLE_CSE_API_KEY
        GOOGLE_CSE_ID
    """

    name = "google_image_search"

    ENDPOINT = "https://www.googleapis.com/customsearch/v1"

    @property
    def api_key(self) -> str:
        return get_settings().GOOGLE_CSE_API_KEY.strip()

    @property
    def cse_id(self) -> str:
        return get_settings().GOOGLE_CSE_ID.strip()

    @property
    def enabled(self) -> bool:
        return get_settings().IMAGE_SEARCH_ENABLED

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.cse_id)

    async def execute(
        self,
        query: str,
        limit: int | None = None,
        image_type: str = "lineart",
        image_size: str = "large",
    ) -> Dict[str, Any]:

        query = query.strip()

        if not query:
            return {
                "success": False,
                "configured": self.configured,
                "query": query,
                "results": [],
                "error": "Image search query cannot be empty.",
            }

        if not self.enabled:
            return {
                "success": False,
                "configured": self.configured,
                "query": query,
                "results": [],
                "error": "Image search is disabled.",
            }

        if not self.configured:
            return {
                "success": False,
                "configured": False,
                "query": query,
                "results": [],
                "error": (
                    "Google image search is not configured. "
                    "Set GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID."
                ),
            }

        if limit is None:
            limit = get_settings().IMAGE_SEARCH_LIMIT

        limit = max(1, min(int(limit), 10))

        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "searchType": "image",
            "num": limit,
            "safe": "active",
            "filter": "1",
            "imgSize": image_size,
            "imgType": image_type,
            "gl": "in",
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    self.ENDPOINT,
                    params=params,
                )

            response.raise_for_status()
            payload = response.json()

        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]

            return {
                "success": False,
                "configured": True,
                "query": query,
                "results": [],
                "error": (
                    f"Google image search returned "
                    f"HTTP {exc.response.status_code}: {detail}"
                ),
            }

        except httpx.RequestError as exc:
            return {
                "success": False,
                "configured": True,
                "query": query,
                "results": [],
                "error": f"Image search request failed: {exc}",
            }

        except Exception as exc:
            return {
                "success": False,
                "configured": True,
                "query": query,
                "results": [],
                "error": f"Image search failed: {exc}",
            }

        results: List[Dict[str, Any]] = []

        for item in payload.get("items", []):
            image = item.get("image", {})

            image_url = item.get("link", "")
            thumbnail_url = image.get("thumbnailLink", "")

            if not image_url:
                continue

            results.append(
                {
                    "title": item.get(
                        "title",
                        "Educational image",
                    ),
                    "image_url": image_url,
                    "thumbnail_url": thumbnail_url,
                    "source_url": image.get(
                        "contextLink",
                        item.get("displayLink", ""),
                    ),
                    "source_name": item.get(
                        "displayLink",
                        "",
                    ),
                    "width": image.get("width"),
                    "height": image.get("height"),
                    "byte_size": image.get("byteSize"),
                }
            )

        return {
            "success": True,
            "configured": True,
            "query": query,
            "results": results,
            "total": len(results),
        }


image_search_tool = GoogleImageSearchTool()