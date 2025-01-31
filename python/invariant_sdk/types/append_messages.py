"""Model class for the AppendMessages API."""

import copy

from typing import Any, List, Dict
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class AppendMessagesRequest(BaseModel):
    """Model class which holds the AppendMessages API request."""

    messages: List[Dict]
    trace_id: str

    # Enable strict type checking.
    model_config = ConfigDict(strict=True)

    @field_validator("messages", mode="before")
    @classmethod
    def validate_and_add_timestamps(cls, messages: List[Dict]) -> List[Dict]:
        """Validate messages and add a timestamp to each."""
        if not messages:
            raise ValueError("messages cannot be empty")
        if not all(isinstance(msg, dict) and msg for msg in messages):
            raise ValueError("messages must be a list of non-empty dictionaries")

        # Deep copy to ensure original data is not modified
        messages_copy = copy.deepcopy(messages)

        # Add default timestamp to each message
        current_time = datetime.now(timezone.utc).isoformat()
        for msg in messages_copy:
            msg.setdefault("timestamp", current_time)
        return messages_copy

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

    def dump_messages(self) -> Dict[str, Any]:
        """
        Return the messages as a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A JSON-serializable dictionary representing the
                            messages.
        """
        dump = self.model_dump()
        del dump["trace_id"]
        return dump
