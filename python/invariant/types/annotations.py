"""Contains the model class for the annotation data."""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class AnnotationCreate(BaseModel):
    """Holds the annotation data for Create APIs."""

    content: str
    address: str
    extra_metadata: Optional[Dict[Any, Any]] = None
