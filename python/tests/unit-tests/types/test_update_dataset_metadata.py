"""Tests for the UpdateDatasetMetadataRequest class."""

import pytest
from invariant_sdk.types.update_dataset_metadata import (
    UpdateDatasetMetadataRequest,
    MetadataUpdate,
)


def test_update_dataset_metadata_request_valid():
    """Test creating the UpdateDatasetMetadataRequest class with valid data."""
    request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        replace_all=True,
        metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=95.5),
    )
    assert request.dataset_name == "example_dataset"
    assert request.metadata.benchmark == "benchmark_name"
    assert request.metadata.accuracy == 95.5
    assert request.replace_all is True


def test_update_dataset_metadata_request_no_benchmark():
    """Test creating the UpdateDatasetMetadataRequest class with no benchmark."""
    request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        metadata=MetadataUpdate(accuracy=95.5),
    )
    assert request.dataset_name == "example_dataset"
    assert request.metadata.benchmark is None
    assert request.metadata.accuracy == 95.5
    assert request.replace_all is False


def test_update_dataset_metadata_request_no_accuracy():
    """Test creating the UpdateDatasetMetadataRequest class with no accuracy."""
    request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        metadata=MetadataUpdate(benchmark="benchmark_name"),
    )
    assert request.dataset_name == "example_dataset"
    assert request.metadata.accuracy is None
    assert request.metadata.benchmark == "benchmark_name"
    assert request.replace_all is False


def test_update_dataset_metadata_request_no_fields():
    """Test creating the UpdateDatasetMetadataRequest class with no fields."""
    with pytest.raises(
        ValueError, match="At least one field must be provided for MetadataUpdate"
    ):
        UpdateDatasetMetadataRequest(
            dataset_name="example_dataset", metadata=MetadataUpdate()
        )


def test_update_dataset_metadata_request_invalid_dataset_name():
    """Test creating the UpdateDatasetMetadataRequest class with an invalid dataset_name."""
    with pytest.raises(ValueError, match="Input should be a valid string"):
        UpdateDatasetMetadataRequest(
            dataset_name=123,
            metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=95.5),
        )


def test_update_dataset_metadata_request_invalid_benchmark():
    """Test creating the UpdateDatasetMetadataRequest class with an invalid benchmark."""
    with pytest.raises(ValueError, match="benchmark must be a non-empty string."):
        UpdateDatasetMetadataRequest(
            dataset_name="example_dataset",
            metadata=MetadataUpdate(benchmark="", accuracy=95.5),
        )

def test_update_dataset_metadata_request_invalid_name():
    """Test creating the UpdateDatasetMetadataRequest class with an invalid benchmark."""
    with pytest.raises(ValueError, match="name must be a non-empty string."):
        UpdateDatasetMetadataRequest(
            dataset_name="example_dataset",
            metadata=MetadataUpdate(benchmark="xyz", accuracy=95.5, name=""),
        )


def test_update_dataset_metadata_request_invalid_accuracy():
    """Test creating the UpdateDatasetMetadataRequest class with an invalid accuracy."""
    with pytest.raises(
        ValueError, match="Accuracy must be a non-negative float or int."
    ):
        UpdateDatasetMetadataRequest(
            dataset_name="example_dataset",
            metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=-1),
        )

def test_update_dataset_metadata_request_invalid_replace_all():
    """Test creating the UpdateDatasetMetadataRequest class with an invalid accuracy."""
    with pytest.raises(
        ValueError, match="should be a valid boolean"
    ):
        UpdateDatasetMetadataRequest(
            dataset_name="example_dataset",
            replace_all="Random",
            metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=1),
        )

def test_update_dataset_metadata_request_no_dataset_name():
    """Test creating the UpdateDatasetMetadataRequest class with no dataset_name."""
    with pytest.raises(ValueError, match="Field required"):
        UpdateDatasetMetadataRequest(
            metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=95.5),
        )


def test_update_dataset_metadata_request_empty_dataset_name():
    """Test creating the UpdateDatasetMetadataRequest class with no dataset_name."""
    with pytest.raises(ValueError, match="Dataset name must be a non-empty string."):
        UpdateDatasetMetadataRequest(
            dataset_name="",
            metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=95.5),
        )


def test_update_dataset_metadata_to_json():
    """Test the UpdateDatasetMetadataRequest to_json method."""
    request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        metadata=MetadataUpdate(benchmark="benchmark_name", accuracy=95.5, name="name"),
    )
    assert request.to_json() == {
        "dataset_name": "example_dataset",
        "metadata": {"benchmark": "benchmark_name", "accuracy": 95.5, "name": "name"},
        "replace_all": False,
    }


def test_metadata_update_to_json():
    """Test the MetadataUpdate to_json method."""
    metadata_update = MetadataUpdate(accuracy=95.5)
    assert metadata_update.to_json() == {"accuracy": 95.5}
