"""Tests for push_traces.py"""

from typing import Dict, List
import pytest
from invariant.types.annotations import AnnotationCreate
from invariant.types.push_traces import PushTracesRequest, PushTracesResponse


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


def test_validate_fields_request_valid_data(
    valid_messages, valid_annotations, valid_metadata
):
    """Test PushTracesRequest.validate_fields with valid data."""
    # Should not raise any exception
    request = PushTracesRequest(
        messages=valid_messages,
        annotations=valid_annotations,
        metadata=valid_metadata,
        dataset="example dataset",
    )

    assert (
        request.messages == valid_messages
        and request.annotations == valid_annotations
        and request.metadata == valid_metadata
        and request.dataset == "example dataset"
    )


def test_validate_fields_request_invalid_messages(valid_annotations, valid_metadata):
    """Test PushTracesRequest.validate_fields with invalid messages."""
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


def test_validate_fields_request_invalid_annotations(valid_messages, valid_metadata):
    """Test PushTracesRequest.validate_fields with invalid annotations."""
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


def test_validate_fields_request_invalid_metadata(valid_messages, valid_annotations):
    """Test PushTracesRequest.validate_fields with invalid metadata."""
    invalid_metadata = [{"meta_key": "meta_value"}, {"meta_key": "meta_value"}]

    with pytest.raises(
        ValueError, match="metadata must be the same length as messages"
    ):
        _ = PushTracesRequest(
            messages=valid_messages,
            annotations=valid_annotations,
            metadata=invalid_metadata,
        )
    with pytest.raises(
        ValueError, match="metadata must be a list of Dict type"
    ):
        _ = PushTracesRequest(
            messages=valid_messages,
            annotations=valid_annotations,
            metadata=[[{"meta_key": "meta_value"}]],
        )


def test_validate_fields_request_none_values(valid_messages):
    """Test PushTracesRequest.validate_fields with None values."""
    # Should not raise any exception
    request = PushTracesRequest(
        messages=valid_messages, annotations=None, metadata=None
    )

    assert (
        request.messages == valid_messages
        and request.annotations is None
        and request.metadata is None
    )


def test_request_to_json(valid_messages, valid_annotations, valid_metadata):
    """Test converting PushTracesRequest to a JSON object."""
    request = PushTracesRequest(
        messages=valid_messages,
        annotations=valid_annotations,
        metadata=valid_metadata,
        dataset="example_dataset",
    )
    json_obj = request.to_json()

    assert json_obj == {
        "messages": [
            [
                {
                    "key1": "value1",
                },
                {
                    "key2": "value2",
                },
            ],
        ],
        "annotations": [
            [
                {
                    "address": "messages[0].content:L0",
                    "extra_metadata": None,
                    "content": "example content",
                },
            ],
        ],
        "dataset": "example_dataset",
        "metadata": [
            {
                "meta_key": "meta_value",
            },
        ],
    }


def test_response_from_json():
    """Test creating PushTracesResponse from a JSON object."""
    json_obj = {"id": ["123", "456"], "dataset": "example_dataset"}
    response = PushTracesResponse.from_json(json_obj)

    assert response.id == ["123", "456"]
    assert response.dataset == "example_dataset"


def test_response_from_json_missing_dataset():
    """Test creating PushTracesResponse from a JSON object without dataset."""
    json_obj = {"id": ["123", "456"]}
    response = PushTracesResponse.from_json(json_obj)

    assert response.id == ["123", "456"] and response.dataset is None


def test_response_from_json_empty_id():
    """Test creating PushTracesResponse from a JSON object with empty id list."""
    json_obj = {"id": [], "dataset": "example_dataset"}
    response = PushTracesResponse.from_json(json_obj)

    assert response.id == [] and response.dataset == "example_dataset"


def test_response_from_invalid_json():
    """Test creating PushTracesResponse from an invalid JSON object."""
    json_obj = {"invalid_field": "invalid_value"}
    with pytest.raises(ValueError):
        PushTracesResponse.from_json(json_obj)
