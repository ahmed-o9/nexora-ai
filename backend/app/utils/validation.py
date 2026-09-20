from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError as PydanticValidationError

from ..core.exceptions import ValidationError


T = TypeVar("T", bound=BaseModel)


def validate(data: Any, model: Type[T]) -> T:
    """
    Validate arbitrary data against a Pydantic model.
    """
    try:
        return model.model_validate(data)
    except PydanticValidationError as exc:
        raise ValidationError(
            f"Invalid structured data: {exc}"
        ) from exc