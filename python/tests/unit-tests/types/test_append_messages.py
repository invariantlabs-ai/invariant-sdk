"""Tests for the AppendMessagesRequest class."""

import pytest
from invariant_sdk.types.append_messages import AppendMessagesRequest
from pydantic import ValidationError


def test_valid_input():
    """Test a valid input."""
    messages = [{"key": "value"}, {"another_key": "another_value"}]
    trace_id = "valid-trace-id"

    request = AppendMessagesRequest(messages=messages, trace_id=trace_id)

    assert request.messages == messages
    assert request.trace_id == trace_id
    assert request.to_json() == {"messages": messages, "trace_id": trace_id}


def test_empty_messages():
    """Test validation when messages is an empty list."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(messages=[], trace_id="valid-trace-id")

    assert "messages cannot be empty" in str(exc_info.value)


def test_messages_not_a_list():
    """Test validation when messages is not a list."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(messages="not-a-list", trace_id="valid-trace-id")

    assert "should be a valid list" in str(exc_info.value)


def test_messages_contains_non_dicts():
    """Test validation when messages contain non-dict elements."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(
            messages=[{"key": "value"}, "not-a-dict"], trace_id="valid-trace-id"
        )

    assert "should be a valid dictionary" in str(exc_info.value)


def test_messages_contains_empty_dict():
    """Test validation when messages contain an empty dictionary."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(
            messages=[{"key": "value"}, {}], trace_id="valid-trace-id"
        )

    assert "messages must be a list of non-empty dictionaries" in str(exc_info.value)


def test_empty_trace_id():
    """Test validation when trace_id is empty."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(messages=[{"key": "value"}], trace_id="")

    assert "trace_id cannot be empty" in str(exc_info.value)


def test_none_trace_id():
    """Test validation when trace_id is None."""
    with pytest.raises(ValidationError) as exc_info:
        AppendMessagesRequest(messages=[{"key": "value"}], trace_id=None)

    assert "should be a valid string" in str(exc_info.value)
