"""Model class for the PushTraces API."""

from typing import Any, Dict, List, Optional
from invariant_sdk.types.annotations import AnnotationCreate
from pydantic import BaseModel


class PushTracesRequest(BaseModel):
    """Model class which holds the PushTraces API request."""

    messages: List[List[Dict]]
    annotations: Optional[List[List[AnnotationCreate]]] = None
    dataset: Optional[str] = None
    metadata: Optional[List[Dict]] = None

    def __init__(self, **data: Any):
        # Call the validation method
        self.validate_fields(
            data.get("messages"), data.get("annotations"), data.get("metadata")
        )
        super().__init__(**data)

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the PushTracesRequest instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A JSON-serializable dictionary representing the PushTracesRequest instance.
        """
        return self.model_dump()

    @staticmethod
    def validate_fields(
        messages: List[List[Dict]],
        annotations: Optional[List[List[AnnotationCreate]]],
        metadata: Optional[List[Dict]],
    ):
        """
        Validate the fields of the PushTracesRequest object.

        Args:
            messages (List[List[Trace]]): The messages to validate.
            annotations (Optional[List[AnnotationCreate]]): The annotations to validate.
            metadata (Optional[List[Metadata]]): The metadata to validate.

        Raises:
            ValueError: If any validation fails.
        """
        if messages is None or len(messages) == 0:
            raise ValueError("messages cannot be empty")
        if not all(
            isinstance(msg, list) and all(isinstance(trace, dict) for trace in msg)
            for msg in messages
        ):
            raise ValueError("messages must be a list of lists of dictionaries")
        if annotations is not None and len(annotations) != len(messages):
            raise ValueError("annotations must be the same length as messages")
        if annotations is not None and not all(
            isinstance(trace_annotation, list)
            and all(
                isinstance(annotation, AnnotationCreate)
                for annotation in trace_annotation
            )
            for trace_annotation in annotations
        ):
            raise ValueError(
                "annotations must be a list of lists of AnnotationCreate type"
            )
        if metadata is not None and len(metadata) != len(messages):
            raise ValueError("metadata must be the same length as messages")
        if metadata is not None and not all(
            isinstance(metadatum, Dict) for metadatum in metadata
        ):
            raise ValueError("metadata must be a list of Dict type")


class PushTracesResponse(BaseModel):
    """Model class which holds the PushTraces API response."""

    id: List[str]
    dataset: Optional[str] = None

    @classmethod
    def from_json(cls, json_obj: Dict) -> "PushTracesResponse":
        """
        Create an instance of PushTracesResponse from a JSON object.

        Args:
            json_obj (Dict): A JSON object representing a PushTracesResponse.

        Returns:
            PushTracesResponse: An instance of PushTracesResponse.
        """
        return cls.model_validate(json_obj)
