"""Model class for the AppendMessages API."""

from typing import Any, List, Dict
from pydantic import BaseModel, ConfigDict, field_validator


class AppendMessagesRequest(BaseModel):
    """Model class which holds the AppendMessages API request."""

    messages: List[Dict]
    trace_id: str

    # Enable strict type checking.
    model_config = ConfigDict(strict=True)

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, messages: List[Dict]) -> List[Dict]:
        """Validate the messages."""
        if not messages:
            raise ValueError("messages cannot be empty")
        if not all(msg for msg in messages):
            raise ValueError("messages must be a list of non-empty dictionaries")
        return messages

    @field_validator("trace_id")
    @classmethod
    def validate_trace_id(cls, trace_id: str) -> str:
        """Validate the trace_id."""
        if not trace_id:
            raise ValueError("trace_id cannot be empty")
        return trace_id

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the AppendMessagesRequest instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A JSON-serializable dictionary representing the
                            AppendMessagesRequest instance.
        """
        return self.model_dump()
