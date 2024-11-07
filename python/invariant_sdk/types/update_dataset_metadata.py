"""Model classes for the UpdateDatasetMetadata API."""

from typing import Dict, Optional, Union
from pydantic import BaseModel, ConfigDict, field_validator


class MetadataUpdate(BaseModel):
    """Model for dataset metadata update."""

    benchmark: Optional[str] = None
    accuracy: Optional[Union[float, int]] = None
    name: Optional[str] = None

    # Enable strict type checking.
    model_config = ConfigDict(strict=True)

    @field_validator("accuracy")
    @staticmethod
    def validate_accuracy(
        value: Optional[Union[float, int]],
    ) -> Optional[Union[float, int]]:
        """Ensure accuracy is non-negative, if provided."""
        if value is not None and value < 0:
            raise ValueError("Accuracy must be a non-negative float or int.")
        return value

    @field_validator("benchmark", "name")
    @staticmethod
    def validate_non_empty_string(value: Optional[str], field) -> Optional[str]:
        """Ensure benchmark is a non-empty string, if provided."""
        if value is not None and not value.strip():
            raise ValueError(f"{field.field_name} must be a non-empty string.")
        return value

    def to_json(self) -> Dict:
        """Convert the instance to a JSON-serializable dictionary."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class UpdateDatasetMetadataRequest(BaseModel):
    """Model for the UpdateDatasetMetadata API request."""

    dataset_name: str
    replace_all: Optional[bool] = False
    metadata: MetadataUpdate

    # Enable strict type checking.
    model_config = ConfigDict(strict=True)

    @field_validator("dataset_name")
    @staticmethod
    def validate_dataset_name(value: str) -> str:
        """Ensure dataset_name is a non-empty string."""
        if not value.strip():
            raise ValueError("Dataset name must be a non-empty string.")
        return value

    def to_json(self) -> Dict:
        """Convert the instance to a JSON-serializable dictionary."""
        return self.model_dump()
