import json
import re
from typing import Any


def parse_llm_json(value: Any) -> dict:
    """
    Convert an LLM response into a Python dictionary.

    Handles:
    - already-parsed dictionaries
    - normal JSON strings
    - JSON inside markdown code fences
    - extra text surrounding a JSON object
    """
    if isinstance(value, dict):
        return value

    if value is None:
        raise ValueError("LLM returned no content.")

    text = str(value).strip()

    if not text:
        raise ValueError("LLM returned empty content.")

    # Remove markdown code fences.
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    try:
        result = json.loads(text)
        if not isinstance(result, dict):
            raise ValueError("Expected a JSON object.")
        return result
    except json.JSONDecodeError:
        pass

    # Try extracting the first JSON object.
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)

    if not match:
        raise ValueError("Could not find a JSON object in LLM response.")

    try:
        result = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned by LLM: {exc}") from exc

    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object.")

    return result