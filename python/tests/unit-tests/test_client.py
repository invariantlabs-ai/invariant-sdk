"""Unit tests for the Client and AsyncClient classes."""

from datetime import datetime, timezone
from unittest import mock

import pytest
import requests
from invariant_sdk.client import Client
from invariant_sdk.async_client import AsyncClient
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
import httpx


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


@pytest.mark.parametrize("is_async", [True, False])
def test_client_init_defaults(set_env_vars, is_async):  # pylint: disable=unused-argument
    """Test Client initialization with default values."""
    if is_async:
        client = AsyncClient()
    else:
        client = Client()

    assert client.api_url == "https://default.api.url"
    assert client.api_key == "test-key"
    assert client.timeout_ms == (5000, 20000)
    assert client._headers == {  # pylint: disable=protected-access
        "Authorization": "Bearer test-key",
        "Accept": "application/json",
    }


@pytest.mark.parametrize("is_async", [True, False])
def test_client_init_custom_values(is_async):  # pylint: disable=unused-argument
    """Test Client initialization with custom values."""
    custom_timeout = (10000, 30000)
    custom_session = requests.Session()

    if is_async:
        client = AsyncClient(
            api_url="https://default.api.url",
            api_key="test-key",
            timeout_ms=custom_timeout,
            session=custom_session,
        )
    else:
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


@pytest.mark.parametrize("is_async", [True, False])
def test_client_init_single_timeout_value(set_env_vars, is_async):  # pylint: disable=unused-argument
    """Test Client initialization with a single timeout value."""
    custom_timeout = 15000

    if is_async:
        client = AsyncClient(
            api_url="https://default.api.url",
            api_key="test-key",
            timeout_ms=custom_timeout,
        )
    else:
        client = Client(
            api_url="https://default.api.url",
            api_key="test-key",
            timeout_ms=custom_timeout,
        )

    assert client.timeout_ms == (custom_timeout, custom_timeout)


@pytest.mark.parametrize("is_async", [True, False])
def test_client_repr(is_async):  # pylint: disable=unused-argument
    """Test the __repr__ method of the Client class."""
    if is_async:
        client = AsyncClient(api_url="https://custom.api.url", api_key="test")
    else:
        client = Client(api_url="https://custom.api.url", api_key="test")
    expected_repr = "Invariant Client API URL: https://custom.api.url"
    assert repr(client) == expected_repr


@pytest.mark.parametrize("is_async", [True, False])
async def test_push_traces_with_default_headers(
    is_async, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test the push_traces method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
        "dataset": "example_dataset",
    }
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)

        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            push_traces_response = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).push_trace(push_traces_request)
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response

        with mock.patch("requests.Session", return_value=mock_session):
            push_traces_response = Client(timeout_ms=(3000, 7000)).push_trace(
                push_traces_request
            )

    assert push_traces_response.id == ["123"]
    assert push_traces_response.dataset == "example_dataset"

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "POST",
        "url": "https://default.api.url/api/v1/push/trace",
        "json": push_traces_request.to_json(),
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_push_traces_with_overridden_headers(
    is_async, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test the push_traces method with override headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
        "dataset": "example_dataset",
    }
    request_kwargs = {
        "headers": {
            "Authorization": "Bearer overridden-key",
            "Content-Type": "text/plain",
            "Accept-Language": "en",
        },
    }
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            # Pass headers in request_kwargs to test that it is passed through to the API.
            push_traces_response = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).push_trace(push_traces_request, request_kwargs=request_kwargs)
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            # Pass headers in request_kwargs to test that it is passed through to the API.
            push_traces_response = Client(timeout_ms=(3000, 7000)).push_trace(
                push_traces_request, request_kwargs=request_kwargs
            )

    assert push_traces_response.id == ["123"]
    assert push_traces_response.dataset == "example_dataset"

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "POST",
        "url": "https://default.api.url/api/v1/push/trace",
        "json": push_traces_request.to_json(),
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer overridden-key",  # Overridden.
            "Accept": "application/json",  # Default.
            "Content-Type": "text/plain",  # Overridden.
            "Accept-Language": "en",  # Overridden.
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_create_request_and_push_trace(is_async, set_env_vars):  # pylint: disable=unused-argument
    """Test the push_traces method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "id": ["123"],
    }
    mock_session = mock.Mock()
    mock_session.request.return_value = mock_response

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
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            push_traces_response = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).create_request_and_push_trace(
                messages=messages,
                annotations=annotations,
                metadata=metadata,
            )
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            push_traces_response = Client(
                timeout_ms=(3000, 7000)
            ).create_request_and_push_trace(
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
    expected_call_args = {
        "method": "POST",
        "url": "https://default.api.url/api/v1/push/trace",
        "json": expected_request.to_json(),
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_push_trace_timeout(is_async, set_env_vars, push_traces_request):  # pylint: disable=unused-argument
    """Test that a timeout raises InvariantAPITimeoutError."""
    if is_async:
        with mock.patch("httpx.AsyncClient") as mock_session_cls:
            mock_session = mock.AsyncMock()
            mock_session.request.side_effect = httpx.ReadTimeout("Request timed out")
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantAPITimeoutError) as exc_info:
                await AsyncClient().push_trace(push_traces_request)
    else:
        with mock.patch("requests.Session") as mock_session_cls:
            mock_session = mock.Mock()
            mock_session.request.side_effect = requests.ReadTimeout("Request timed out")
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantAPITimeoutError) as exc_info:
                Client().push_trace(push_traces_request)

    assert (
        str(exc_info.value)
        == "Timeout when calling method: POST for path: /api/v1/push/trace. Server took too long."
    )


@pytest.mark.parametrize("is_async", [True, False])
async def test_push_trace_connection_error(is_async, set_env_vars, push_traces_request):  # pylint: disable=unused-argument
    """Test that a ConnectionError raises InvariantError."""
    if is_async:
        with mock.patch("httpx.AsyncClient") as mock_session_cls:
            mock_session = mock.AsyncMock()
            mock_session.request.side_effect = httpx.ConnectError(
                "Some connection error"
            )
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantError) as exc_info:
                await AsyncClient().push_trace(push_traces_request)
    else:
        with mock.patch("requests.Session") as mock_session_cls:
            mock_session = mock.Mock()
            mock_session.request.side_effect = requests.ConnectionError(
                "Some connection error"
            )
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantError) as exc_info:
                Client().push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Connection error when calling method: POST for path: /api/v1/push/trace."
    )


@pytest.mark.parametrize("is_async", [True, False])
async def test_push_trace_connect_timeout_error(
    is_async, set_env_vars, push_traces_request
):  # pylint: disable=unused-argument
    """Test that a ConnectTimeout raises InvariantError."""
    if is_async:
        with mock.patch("httpx.AsyncClient") as mock_session_cls:
            mock_session = mock.AsyncMock()
            mock_session.request.side_effect = httpx.ConnectTimeout(
                "Timeout connecting to server"
            )
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantError) as exc_info:
                await AsyncClient().push_trace(push_traces_request)
    else:
        with mock.patch("requests.Session") as mock_session_cls:
            mock_session = mock.Mock()
            mock_session.request.side_effect = requests.ConnectTimeout(
                "Timeout connecting to server"
            )
            mock_session_cls.return_value = mock_session
            with pytest.raises(InvariantError) as exc_info:
                Client().push_trace(push_traces_request)
    assert (
        str(exc_info.value)
        == "Timeout when connecting to server for method: POST on path: /api/v1/push/trace."
    )


@pytest.mark.parametrize(
    "is_async, status_code, message, exception_cls, exception_message",
    [
        (True, 401, "Unauthorized", InvariantAuthError, "Authentication failed (401)"),
        (False, 401, "Unauthorized", InvariantAuthError, "Authentication failed (401)"),
        (True, 404, "Not found", InvariantNotFoundError, "Resource not found (404)"),
        (False, 404, "Not found", InvariantNotFoundError, "Resource not found (404)"),
        (True, 429, "Too many requests", InvariantError, "HTTP error when"),
        (False, 429, "Too many requests", InvariantError, "HTTP error when"),
        (True, 500, "Server error", InvariantAPIError, "Server error (500)"),
        (False, 500, "Server error", InvariantAPIError, "Server error (500)"),
    ],
)
async def test_push_trace_auth_error(
    is_async,
    status_code,
    message,
    exception_cls,
    exception_message,
    set_env_vars,
    push_traces_request,
):  # pylint: disable=unused-argument
    """Test that an authentication error raises InvariantAuthError."""
    mock_response = mock.Mock()
    mock_response.status_code = status_code
    if is_async:
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message=message,
            request=mock.Mock(),
            response=mock_response,
        )
        mock_session = mock.AsyncMock(spec=httpx.AsyncClient)
        mock_session.request.return_value = mock_response
        patch_target = "httpx.AsyncClient"
        client_cls = AsyncClient
    else:
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            request=mock.Mock(), response=mock_response
        )
        mock_session = mock.Mock(spec=requests.Session)
        mock_session.request.return_value = mock_response
        patch_target = "requests.Session"
        client_cls = Client

    with mock.patch(patch_target, return_value=mock_session):
        client = client_cls()

        async def run_test():
            with pytest.raises(exception_cls) as exc_info:
                if is_async:
                    await client.push_trace(push_traces_request)
                else:
                    client.push_trace(push_traces_request)

            assert exception_message in str(exc_info.value)

        await run_test()


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


@pytest.mark.parametrize("is_async", [True, False])
async def test_get_dataset_metadata(is_async, set_env_vars):  # pylint: disable=unused-argument
    """Test the get_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "benchmark_name",
        "accuracy": 95.5,
    }
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            metadata = await AsyncClient(timeout_ms=(3000, 7000)).get_dataset_metadata(
                dataset_name="example_dataset",
            )
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            metadata = Client(timeout_ms=(3000, 7000)).get_dataset_metadata(
                dataset_name="example_dataset",
            )
    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "benchmark_name"
    assert metadata.get("accuracy") == 95.5

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "GET",
        "url": "https://default.api.url/api/v1/dataset/metadata/example_dataset",
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_update_dataset_metadata(is_async, set_env_vars):  # pylint: disable=unused-argument
    """Test the update_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "new_benchmark_name",
        "accuracy": 99.5,
    }
    update_metadata_request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        replace_all=True,
        metadata=MetadataUpdate(benchmark="new_benchmark_name", accuracy=99.5),
    )

    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            metadata = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).update_dataset_metadata(update_metadata_request)
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            metadata = Client(timeout_ms=(3000, 7000)).update_dataset_metadata(
                update_metadata_request
            )

    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "new_benchmark_name"
    assert metadata.get("accuracy") == 99.5

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "PUT",
        "url": "https://default.api.url/api/v1/dataset/metadata/example_dataset",
        "json": {
            "metadata": {"benchmark": "new_benchmark_name", "accuracy": 99.5},
            "replace_all": True,
        },
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_update_dataset_metadata_with_overridden_headers(is_async, set_env_vars):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with override headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "benchmark": "new_benchmark_name",
        "accuracy": 99.5,
        "name": "new_name",
    }
    update_metadata_request = UpdateDatasetMetadataRequest(
        dataset_name="example_dataset",
        metadata=MetadataUpdate(accuracy=99.5, name="new_name"),
    )
    # Pass headers in request_kwargs to test that it is passed through to the API.
    request_kwargs = {
        "headers": {
            "Authorization": "Bearer overridden-key",
            "Content-Type": "text/plain",
            "Accept-Language": "en",
        },
    }
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            metadata = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).update_dataset_metadata(
                update_metadata_request, request_kwargs=request_kwargs
            )
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            metadata = Client(timeout_ms=(3000, 7000)).update_dataset_metadata(
                update_metadata_request, request_kwargs=request_kwargs
            )

    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("benchmark") == "new_benchmark_name"
    assert metadata.get("accuracy") == 99.5
    assert metadata.get("name") == "new_name"

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "PUT",
        "url": "https://default.api.url/api/v1/dataset/metadata/example_dataset",
        "json": {
            "metadata": {"accuracy": 99.5, "name": "new_name"},
            "replace_all": False,
        },
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer overridden-key",  # Overridden.
            "Accept": "application/json",  # Default.
            "Content-Type": "text/plain",  # Overridden.
            "Accept-Language": "en",  # Overridden.
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@pytest.mark.parametrize("is_async", [True, False])
async def test_create_request_and_update_dataset_metadata(is_async, set_env_vars):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with default headers passed."""
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "created_on": "2024-11-06 13:40:52",
        "accuracy": 99.5,
    }
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            metadata = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).create_request_and_update_dataset_metadata(
                dataset_name="example_dataset",
                metadata={"benchmark": "some_benchmark"},
            )
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            metadata = Client(
                timeout_ms=(3000, 7000)
            ).create_request_and_update_dataset_metadata(
                dataset_name="example_dataset",
                metadata={"benchmark": "some_benchmark"},
            )

    assert metadata.get("created_on") == "2024-11-06 13:40:52"
    assert metadata.get("accuracy") == 99.5

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "PUT",
        "url": "https://default.api.url/api/v1/dataset/metadata/example_dataset",
        "json": {
            "metadata": {"benchmark": "some_benchmark"},
            "replace_all": False,
        },
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@mock.patch("invariant_sdk.types.append_messages.datetime")
@pytest.mark.parametrize(
    "is_async,with_annotations",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
async def test_append_messages(
    mock_datetime: mock.Mock, is_async: bool, with_annotations: bool, set_env_vars
):  # pylint: disable=unused-argument
    """Test the append_messages method with default headers passed."""
    # Mock datetime to return a specific value for `now()`
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "success": True,
    }
    update_metadata_request = AppendMessagesRequest(
        messages=[
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ],
        trace_id="123",
        annotations=AnnotationCreate.from_dicts(
            [
                {
                    "content": "annotating one",
                    "address": "messages[0].content:L0",
                    "extra_metadata": {"key1": "value1"},
                }
            ]
        )
        if with_annotations
        else None,
    )
    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            result = await AsyncClient(timeout_ms=(3000, 7000)).append_messages(
                update_metadata_request
            )
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            result = Client(timeout_ms=(3000, 7000)).append_messages(
                update_metadata_request
            )

    assert result.get("success")

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "POST",
        "url": "https://default.api.url/api/v1/trace/123/messages",
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        "json": {
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
            "annotations": [
                {
                    "content": "annotating one",
                    "address": "messages[0].content:L0",
                    "extra_metadata": {"key1": "value1"},
                }
            ]
            if with_annotations
            else [],
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)


@mock.patch("invariant_sdk.types.append_messages.datetime")
@pytest.mark.parametrize(
    "is_async,with_annotations",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
async def test_create_request_and_append_messages(
    mock_datetime: mock.Mock, is_async: bool, with_annotations: bool, set_env_vars
):  # pylint: disable=unused-argument
    """Test the create_request_and_update_dataset_metadata method with default headers passed."""
    # Mock datetime to return a specific value for `now()`
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "success": True,
    }
    request = {
        "messages": [
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ],
        "trace_id": "123",
        "annotations": [
            {
                "content": "annotating one",
                "address": "messages[0].content:L0",
                "extra_metadata": {"key1": "value1"},
            }
        ]
        if with_annotations
        else None,
    }

    if is_async:
        mock_session = mock.AsyncMock()
        mock_session.request = mock.AsyncMock(return_value=mock_response)
        with mock.patch("httpx.AsyncClient", return_value=mock_session):
            result = await AsyncClient(
                timeout_ms=(3000, 7000)
            ).create_request_and_append_messages(**request)
    else:
        mock_session = mock.Mock()
        mock_session.request.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_session):
            result = Client(timeout_ms=(3000, 7000)).create_request_and_append_messages(
                **request
            )

    assert result.get("success")

    # Assert that the request method was called once with the expected arguments.
    expected_call_args = {
        "method": "POST",
        "url": "https://default.api.url/api/v1/trace/123/messages",
        "timeout": (3.0, 7.0),
        "headers": {
            "Authorization": "Bearer test-key",  # Default API key from env.
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        "json": {
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
            "annotations": [
                {
                    "content": "annotating one",
                    "address": "messages[0].content:L0",
                    "extra_metadata": {"key1": "value1"},
                }
            ]
            if with_annotations
            else [],
        },
    }
    if not is_async:  # Only add `stream=False` for sync clients (requests.Session)
        expected_call_args["stream"] = False
    mock_session.request.assert_called_once_with(**expected_call_args)
