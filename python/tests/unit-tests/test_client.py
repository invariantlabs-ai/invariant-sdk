"""Unit tests for the Client class."""

from datetime import datetime, timezone
from unittest import mock

import pytest
import requests
from invariant_sdk.client import Client
from invariant_sdk.types.annotations import AnnotationCreate
from invariant_sdk.types.push_traces import PushTracesRequest
from invariant_sdk.types.update_dataset_metadata import (
    UpdateDatasetMetadataRequest,
    MetadataUpdate,
)
from invariant_sdk.types.append_messages import AppendMessagesRequest
from invariant_sdk.types.exceptions import (
    InvariantAPITimeoutError,
    InvariantNotFoundError,
    InvariantAuthError,
    InvariantAPIError,
    InvariantError,
)


@pytest.fixture(name="set_env_vars")
def fixture_set_env_vars(monkeypatch):
    """Fixture to set environment variables for tests."""
    monkeypatch.setenv("INVARIANT_API_ENDPOINT", "https://default.api.url")
    monkeypatch.setenv("INVARIANT_API_KEY", "test-key")


@pytest.fixture(name="push_traces_request")
def fixture_push_traces_request():
    """Fixture for a PushTracesRequest instance."""
    return PushTracesRequest(
        messages=[
            [
                {"role": "user", "content": "one"},
                {"role": "assistant", "content": "two \n three"},
            ]
        ],
        annotations=[
            [
                AnnotationCreate(
                    content="annotating one",
                    address="messages[0].content:L0",
                    extra_metadata={"key1": "value1"},
                )
            ]
        ],
        dataset="example_dataset",
    )


def test_client_init_defaults(set_env_vars):  # pylint: disable=unused-argument
    """Test Client initialization with default values."""
    client = Client()

    assert client.api_url == "https://default.api.url"
    assert client.api_key == "test-key"
    assert client.timeout_ms == (5000, 20000)
    assert client._headers == {  # pylint: disable=protected-access
        "Authorization": "Bearer test-key",
        "Accept": "application/json",
    }


def test_client_init_custom_values():
    """Test Client initialization with custom values."""
    custom_timeout = (10000, 30000)
    custom_session = requests.Session()

    client = Client(
        api_url="https://default.api.url",
        api_key="test-key",
        timeout_ms=custom_timeout,
        session=custom_session,
    )

    assert client.api_url == "https://default.api.url"
    assert client.api_key == "test-key"
    assert client.timeout_ms == custom_timeout
    assert client.session == custom_session


def test_client_init_single_timeout_value(set_env_vars):  # pylint: disable=unused-argument
    """Test Client initialization with a single timeout value."""
    custom_timeout = 15000

    client = Client(
        api_url="https://default.api.url", api_key="test-key", timeout_ms=custom_timeout
    )

    assert client.timeout_ms == (custom_timeout, custom_timeout)


def test_client_repr():
    """Test the __repr__ method of the Client class."""
    client = Client(api_url="https://custom.api.url", api_key="test")
    expected_repr = "Invariant Client API URL: https://custom.api.url"
    assert repr(client) == expected_repr


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_traces_with_default_headers(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test the push_traces method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
        "dataset": "example_dataset",
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))
    push_traces_response = client.push_trace(
        push_traces_request,
    )
    assert push_traces_response.id == ["123"]
    assert push_traces_response.dataset == "example_dataset"

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://default.api.url/api/v1/push/trace",
        json=push_traces_request.to_json(),
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_traces_with_overridden_headers(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test the push_traces method with override headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
        "dataset": "example_dataset",
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))
    # Pass headers in request_kwargs to test that it is passed through to the API.
    push_traces_response = client.push_trace(
        push_traces_request,
        request_kwargs={
            "headers": {
                "Authorization": "Bearer overridden-key",
                "Content-Type": "text/plain",
                "Accept-Language": "en",
            },
        },
    )
    assert push_traces_response.id == ["123"]
    assert push_traces_response.dataset == "example_dataset"

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://default.api.url/api/v1/push/trace",
        json=push_traces_request.to_json(),
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer overridden-key",  # Overridden.
            "Accept": "application/json",  # Default.
            "Content-Type": "text/plain",  # Overridden.
            "Accept-Language": "en",  # Overridden.
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_create_request_and_push_trace(mock_session_cls: mock.Mock, set_env_vars):  # pylint: disable=unused-argument
    """Test the push_traces method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))
    messages = [
        [
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ]
    ]
    annotations = [
        [
            {
                "content": "annotating one",
                "address": "messages[0].content:L0",
                "extra_metadata": {"key1": "value1"},
            }
        ]
    ]
    metadata = [{"x": "y"}]
    push_traces_response = client.create_request_and_push_trace(
        messages=messages,
        annotations=annotations,
        metadata=metadata,
    )
    assert push_traces_response.id == ["123"]

    # Assert that the request method was called once with the expected arguments.
    expected_request = PushTracesRequest(
        messages=messages,
        annotations=AnnotationCreate.from_nested_dicts(annotations),
        metadata=metadata,
    )
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://default.api.url/api/v1/push/trace",
        timeout=(3.0, 7.0),
        json=expected_request.to_json(),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_timeout(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a timeout raises InvariantAPITimeoutError."""
    mock_session = mock.Mock()
    mock_session.request.side_effect = requests.ReadTimeout
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantAPITimeoutError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Timeout when calling method: POST for path: /api/v1/push/trace. Server took too long."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_connection_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a ConnectionError raises InvariantError."""
    mock_session = mock.Mock()
    mock_session.request.side_effect = requests.ConnectionError
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Connection error when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_connect_timeout_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a ConnectTimeout raises InvariantError."""
    mock_session = mock.Mock()
    mock_session.request.side_effect = requests.ConnectTimeout
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Timeout when connecting to server for method: POST on path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_auth_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that an authentication error raises InvariantAuthError."""
    mock_response = mock.Mock()
    mock_response.status_code = 401
    http_error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantAuthError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Authentication failed (401) when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_not_found_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a not found error raises InvariantNotFoundError."""
    mock_response = mock.Mock()
    mock_response.status_code = 404
    http_error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantNotFoundError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Resource not found (404) when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_too_many_requests_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a too many requests error raises InvariantError."""
    mock_response = mock.Mock()
    mock_response.status_code = 429
    http_error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "HTTP error when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_server_side_error(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a server side error raises InvariantAPIError."""
    mock_response = mock.Mock()
    mock_response.status_code = 500
    http_error = requests.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error

    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantAPIError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Server error (500) when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_push_trace_generic_exception(
    mock_session_cls: mock.Mock, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a generic exception raises InvariantError."""
    mock_session = mock.Mock()
    mock_session.request.side_effect = Exception("Generic error")
    mock_session_cls.return_value = mock_session

    client = Client()

    with pytest.raises(InvariantError) as exc_info:
        client.push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Unexpected error (Exception): Generic error when calling method: POST for path: /api/v1/push/trace."
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_get_dataset_metadata(mock_session_cls: mock.Mock, set_env_vars):  # pylint: disable=unused-argument
    """Test the get_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "benchmark_name",
        "accuracy": 95.5,
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))
    metadata = client.get_dataset_metadata(
        dataset_name="example_dataset",
    )
    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "benchmark_name"
    assert metadata.get("accuracy") == 95.5

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://default.api.url/api/v1/dataset/metadata/example_dataset",
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_update_dataset_metadata(mock_session_cls: mock.Mock, set_env_vars):  # pylint: disable=unused-argument
    """Test the update_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "new_benchmark_name",
        "accuracy": 99.5,
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))

    update_metadata_request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        replace_all=True,
        metadata=MetadataUpdate(benchmark="new_benchmark_name", accuracy=99.5),
    )

    metadata = client.update_dataset_metadata(update_metadata_request)
    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "new_benchmark_name"
    assert metadata.get("accuracy") == 99.5

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://default.api.url/api/v1/dataset/metadata/example_dataset",
        json={
            "metadata": {"benchmark": "new_benchmark_name", "accuracy": 99.5},
            "replace_all": True,
        },
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_update_dataset_metadata_with_overridden_headers(
    mock_session_cls: mock.Mock, set_env_vars
):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with override headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "new_benchmark_name",
        "accuracy": 99.5,
        "name": "new_name",
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))

    update_metadata_request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        metadata=MetadataUpdate(accuracy=99.5, name="new_name"),
    )

    # Pass headers in request_kwargs to test that it is passed through to the API.
    metadata = client.update_dataset_metadata(
        update_metadata_request,
        request_kwargs={
            "headers": {
                "Authorization": "Bearer overridden-key",
                "Content-Type": "text/plain",
                "Accept-Language": "en",
            },
        },
    )
    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "new_benchmark_name"
    assert metadata.get("accuracy") == 99.5
    assert metadata.get("name") == "new_name"

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://default.api.url/api/v1/dataset/metadata/example_dataset",
        json={"metadata": {"accuracy": 99.5, "name": "new_name"}, "replace_all": False},
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer overridden-key",  # Overridden.
            "Accept": "application/json",  # Default.
            "Content-Type": "text/plain",  # Overridden.
            "Accept-Language": "en",  # Overridden.
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
def test_create_request_and_update_dataset_metadata(
    mock_session_cls: mock.Mock, set_env_vars
):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "accuracy": 99.5,
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    client = Client(timeout_ms=(3000, 7000))

    metadata = client.create_request_and_update_dataset_metadata(
        dataset_name="example_dataset",
        metadata={"benchmark": "some_benchmark"},
    )

    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("accuracy") == 99.5

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://default.api.url/api/v1/dataset/metadata/example_dataset",
        timeout=(3.0, 7.0),
        json={
            "metadata": {"benchmark": "some_benchmark"},
            "replace_all": False,
        },
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        stream=False,
    )


@mock.patch("invariant_sdk.client.requests.Session")
@mock.patch("invariant_sdk.types.append_messages.datetime")
def test_append_messages(
    mock_datetime: mock.Mock, mock_session_cls: mock.Mock, set_env_vars
):  # pylint: disable=unused-argument
    """Test the append_messages method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "success": True,
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    # Mock datetime to return a specific value for `now()`
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "success": True,
    }

    client = Client(timeout_ms=(3000, 7000))

    update_metadata_request = AppendMessagesRequest(
        messages=[
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ],
        trace_id="123",
    )

    result = client.append_messages(update_metadata_request)
    assert result.get("success")

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://default.api.url/api/v1/trace/123/messages",
        stream=False,
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "one",
                    "timestamp": "2025-01-01T12:00:00+00:00",
                },
                {
                    "role": "assistant",
                    "content": "two \n three",
                    "timestamp": "2025-01-01T12:00:00+00:00",
                },
            ],
        },
    )


@mock.patch("invariant_sdk.client.requests.Session")
@mock.patch("invariant_sdk.types.append_messages.datetime")
def test_create_request_and_append_messages(
    mock_datetime: mock.Mock, mock_session_cls: mock.Mock, set_env_vars
):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "success": True,
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response
    mock_session_cls.return_value = mock_session

    # Mock datetime to return a specific value for `now()`
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    client = Client(timeout_ms=(3000, 7000))

    result = client.create_request_and_append_messages(
        messages=[
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ],
        trace_id="123",
    )

    assert result.get("success")

    # Assert that the request method was called once with the expected arguments.
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://default.api.url/api/v1/trace/123/messages",
        stream=False,
        timeout=(3.0, 7.0),
        headers={
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "one",
                    "timestamp": "2025-01-01T12:00:00+00:00",
                },
                {
                    "role": "assistant",
                    "content": "two \n three",
                    "timestamp": "2025-01-01T12:00:00+00:00",
                },
            ],
        },
    )
