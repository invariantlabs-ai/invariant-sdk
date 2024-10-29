"""Test cases for Annotation classes."""

import pytest
from invariant_sdk.types.annotations import AnnotationCreate


def test_annotation_create_initialization():
    """Test the initialization of AnnotationCreate without extra metadata."""
    annotation = AnnotationCreate(content="Test content", address="Test address")
    assert annotation.content == "Test content"
    assert annotation.address == "Test address"
    assert annotation.extra_metadata is None


def test_annotation_create_with_metadata():
    """Test the initialization of AnnotationCreate with extra metadata."""
    metadata = {"key": "value"}
    annotation = AnnotationCreate(
        content="Test content", address="Test address", extra_metadata=metadata
    )
    assert annotation.extra_metadata == metadata


def test_annotation_create_from_nested_dicts():
    """Test the from_nested_dicts class method with valid input."""
    data = [
        [
            {"content": "Content 1", "address": "Address 1"},
            {
                "content": "Content 2",
                "address": "Address 2",
                "extra_metadata": {"key": "value"},
            },
        ],
        [{"content": "Content 3", "address": "Address 3"}],
    ]
    annotations = AnnotationCreate.from_nested_dicts(data)
    assert len(annotations) == 2
    assert len(annotations[0]) == 2
    assert len(annotations[1]) == 1
    assert annotations[0][0].content == "Content 1"
    assert annotations[0][1].extra_metadata == {"key": "value"}


def test_annotation_create_from_nested_dicts_invalid_input():
    """Test the from_nested_dicts class method with invalid input."""
    with pytest.raises(ValueError):
        AnnotationCreate.from_nested_dicts(
            [{"content": "Content 1", "address": "Address 1"}]
        )
