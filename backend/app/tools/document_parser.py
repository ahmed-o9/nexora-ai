import csv
import json
from pathlib import Path


class DocumentParserTool:
    """Extract useful text from common educational document formats."""

    name = "document_parser"

    async def execute(self, path: str):
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = file_path.suffix.lower()

        if suffix in {".txt", ".md", ".py", ".c", ".cpp", ".java"}:
            text = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

        elif suffix == ".json":
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            )
            text = json.dumps(data, indent=2, ensure_ascii=False)

        elif suffix == ".csv":
            rows = []
            with file_path.open(
                "r",
                encoding="utf-8",
                errors="replace",
                newline="",
            ) as handle:
                reader = csv.reader(handle)
                rows = [" | ".join(row) for row in reader]

            text = "\n".join(rows)

        elif suffix == ".pdf":
            text = await self._parse_pdf(file_path)

        else:
            raise ValueError(
                f"Unsupported document type: {suffix}"
            )

        return {
            "filename": file_path.name,
            "type": suffix.lstrip("."),
            "characters": len(text),
            "text": text,
        }

    async def _parse_pdf(self, path: Path) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError(
                "PDF support requires pypdf. "
                "Run: pip install pypdf"
            ) from exc

        reader = PdfReader(str(path))

        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n\n".join(pages)