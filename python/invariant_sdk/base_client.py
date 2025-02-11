"""Base client for interacting with the Invariant APIs."""

from typing import Dict, Mapping, Optional, Tuple, Union
from invariant_sdk.types.exceptions import (
    InvariantError,
    InvariantAPIError,
    InvariantAuthError,
    InvariantNotFoundError,
)
from invariant_sdk.types.push_traces import PushTracesRequest
from invariant_sdk.types.update_dataset_metadata import (
    UpdateDatasetMetadataRequest,
)
from invariant_sdk.types.append_messages import AppendMessagesRequest
import invariant_sdk.utils as invariant_utils

DEFAULT_CONNECTION_TIMEOUT_MS = 5_000
DEFAULT_READ_TIMEOUT_MS = 20_000
PUSH_TRACE_API_PATH = "/api/v1/push/trace"
DATASET_METADATA_API_PATH = "/api/v1/dataset/metadata"
TRACE_API_PATH = "/api/v1/trace"


class BaseClient:
    """Base client for interacting with the Invariant APIs."""

    __slots__ = ["api_url", "api_key", "timeout_ms"]

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_ms: Optional[Union[int, Tuple[int, int]]] = None,
    ) -> None:
        self.api_url = invariant_utils.get_api_url(api_url)
        self.api_key = invariant_utils.get_api_key(api_key)
        self.timeout_ms = (
            (timeout_ms, timeout_ms)
            if isinstance(timeout_ms, int)
            else (
                timeout_ms or (DEFAULT_CONNECTION_TIMEOUT_MS, DEFAULT_READ_TIMEOUT_MS)
            )
        )

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def __repr__(self) -> str:
        return f"Invariant Client API URL: {self.api_url}"

    def _handle_http_error(self, method: str, pathname: str, response) -> None:
        if response.status_code == 500:
            raise InvariantAPIError(
                f"Server error (500) when calling method: {method} for path: {pathname}."
            )
        if response.status_code == 401:
            raise InvariantAuthError(
                f"Authentication failed (401) when calling method: {method} for path: {pathname}."
            )
        if response.status_code == 404:
            raise InvariantNotFoundError(
                f"Resource not found (404) when calling method: {method} for path: {pathname}."
            )
        raise InvariantError(
            f"HTTP error when calling method: {method} for path: {pathname}."
        )

    def _prepare_request_kwargs(self, request_kwargs: Optional[Mapping]) -> Dict:
        request_kwargs = request_kwargs or {}
        return {
            "timeout": (self.timeout_ms[0] / 1000, self.timeout_ms[1] / 1000),
            **request_kwargs,
            "headers": {
                **self._headers,
                **request_kwargs.get("headers", {}),
            },
        }

    def _prepare_push_trace_request(
        self, request: PushTracesRequest, request_kwargs: Optional[Mapping] = None
    ) -> Dict:
        request_kwargs = request_kwargs or {}
        return {
            **request_kwargs,
            "headers": {
                "Content-Type": "application/json",
                **request_kwargs.get("headers", {}),
            },
            "json": request.to_json(),
        }

    def _prepare_get_dataset_metadata_request(
        self, request_kwargs: Optional[Mapping] = None
    ) -> Dict:
        request_kwargs = request_kwargs or {}
        return {
            **request_kwargs,
            "headers": {
                "Content-Type": "application/json",
                **request_kwargs.get("headers", {}),
            },
        }

    def _prepare_update_dataset_metadata_request(
        self,
        request: UpdateDatasetMetadataRequest,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        request_kwargs = request_kwargs or {}
        return {
            **request_kwargs,
            "headers": {
                "Content-Type": "application/json",
                **request_kwargs.get("headers", {}),
            },
            "json": {
                "metadata": request.metadata.to_json(),
                "replace_all": request.replace_all,
            },
        }

    def _prepare_append_messages_request(
        self, request: AppendMessagesRequest, request_kwargs: Optional[Mapping] = None
    ) -> Dict:
        request_kwargs = request_kwargs or {}
        return {
            **request_kwargs,
            "headers": {
                "Content-Type": "application/json",
                **request_kwargs.get("headers", {}),
            },
            "json": {
                "messages": request.dump_messages()["messages"],
            },
        }
