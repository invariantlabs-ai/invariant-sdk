"""Contains the model class for the annotation data."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AnnotationCreate(BaseModel):
    """Holds the annotation data for Create APIs."""

    content: str
    address: str
    extra_metadata: Optional[Dict[Any, Any]] = None

    @classmethod
    def from_nested_dicts(
        cls, data: List[List[Dict[Any, Any]]]
    ) -> List[List["AnnotationCreate"]]:
        """Converts a List of List of Dict to List of List of AnnotationCreate."""
        if not isinstance(data, list) or not all(isinstance(i, list) for i in data):
            raise ValueError("Input must be a List of List of Dict.")
        return [[cls(**item) for item in sublist] for sublist in data]
