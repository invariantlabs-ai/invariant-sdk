"""Tests for push_traces.py"""

from typing import Dict, List
import pytest
from invariant.types.annotations import AnnotationCreate
from invariant.types.push_traces import PushTracesRequest


@pytest.fixture(name="valid_messages")
def fixture_valid_messages() -> List[List[Dict[str, str]]]:
    """Fixture for valid messages."""
    return [[{"key1": "value1"}, {"key2": "value2"}]]


@pytest.fixture(name="valid_annotations")
def fixture_valid_annotations() -> List[List[AnnotationCreate]]:
    """Fixture for valid annotations."""
    return [
        [AnnotationCreate(content="example content", address="messages[0].content:L0")]
    ]


@pytest.fixture(name="valid_metadata")
def fixture_valid_metadata() -> List[Dict[str, str]]:
    """Fixture for valid metadata."""
    return [{"meta_key": "meta_value"}]


def test_validate_fields_valid_data(valid_messages, valid_annotations, valid_metadata):
    """Test validate_fields with valid data."""
    # Should not raise any exception
    _ = PushTracesRequest(
        messages=valid_messages,
        annotations=valid_annotations,
        metadata=valid_metadata,
        dataset="example dataset",
    )


def test_validate_fields_invalid_messages(valid_annotations, valid_metadata):
    """Test validate_fields with invalid messages."""
    invalid_messages = [{"key1": "value1"}, {"key2": "value2"}]

    with pytest.raises(
        ValueError, match="messages must be a list of lists of dictionaries"
    ):
        _ = PushTracesRequest(
            messages=invalid_messages,
            annotations=valid_annotations,
            metadata=valid_metadata,
        )

    with pytest.raises(ValueError, match="messages cannot be empty"):
        _ = PushTracesRequest(
            messages=None, annotations=valid_annotations, metadata=valid_metadata
        )

    with pytest.raises(ValueError, match="messages cannot be empty"):
        _ = PushTracesRequest(
            messages=[], annotations=valid_annotations, metadata=valid_metadata
        )


def test_validate_fields_invalid_annotations(valid_messages, valid_metadata):
    """Test validate_fields with invalid annotations."""
    invalid_annotations = []

    with pytest.raises(
        ValueError, match="annotations must be the same length as messages"
    ):
        _ = PushTracesRequest(
            messages=valid_messages,
            annotations=invalid_annotations,
            metadata=valid_metadata,
        )
    with pytest.raises(
        ValueError, match="annotations must be a list of lists of AnnotationCreate type"
    ):
        _ = PushTracesRequest(
            messages=valid_messages,
            annotations=[
                {"content": "example content", "addres": "messages[0].content:L0"}
            ],
            metadata=valid_metadata,
        )


def test_validate_fields_invalid_metadata(valid_messages, valid_annotations):
    """Test validate_fields with invalid metadata."""
    invalid_metadata = [{"meta_key": "meta_value"}, {"meta_key": "meta_value"}]

    with pytest.raises(
        ValueError, match="metadata must be the same length as messages"
    ):
        _ = PushTracesRequest(
            messages=valid_messages,
            annotations=valid_annotations,
            metadata=invalid_metadata,
        )


def test_validate_fields_none_values(valid_messages):
    """Test validate_fields with None values."""
    # Should not raise any exception
    _ = PushTracesRequest(messages=valid_messages, annotations=None, metadata=None)
