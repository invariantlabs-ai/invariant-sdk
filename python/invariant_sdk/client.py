"""Client for interacting with the Invariant APIs."""

import atexit
from typing import Dict, List, Literal, Mapping, Optional, Tuple, Union
from invariant_sdk.types.annotations import AnnotationCreate
from invariant_sdk.types.exceptions import (
    InvariantError,
    InvariantAPITimeoutError,
    InvariantAPIError,
    InvariantAuthError,
    InvariantNotFoundError,
)
from invariant_sdk.types.push_traces import PushTracesRequest, PushTracesResponse
from invariant_sdk.types.update_dataset_metadata import (
    MetadataUpdate,
    UpdateDatasetMetadataRequest,
)
from invariant_sdk.types.append_messages import AppendMessagesRequest

import requests
import invariant_sdk.utils as invariant_utils


DEFAULT_CONNECTION_TIMEOUT_MS = 5_000
DEFAULT_READ_TIMEOUT_MS = 20_000
PUSH_TRACE_API_PATH = "/api/v1/push/trace"
DATASET_METADATA_API_PATH = "/api/v1/dataset/metadata"
TRACE_API_PATH = "/api/v1/trace"


def _close_session(session: requests.Session) -> None:
    """
    Close the given requests session.

    This function ensures that the provided requests session is properly closed,
    releasing any resources associated with it.

    Args:
        session (requests.Session): The requests session to be closed.
    """
    session.close()


class Client:
    """Client for interacting with the Invariant APIs."""

    __slots__ = ["api_url", "api_key", "timeout_ms", "session"]

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_ms: Optional[Union[int, Tuple[int, int]]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        """
        Initialize a Client instance.

        Args:
            api_url (Optional[str]): URL for the Invariant API. Defaults to the
                                    INVARIANT_API_ENDPOINT environment variable or
                                    DEFAULT_INVARIANT_API_URL if not set.
            api_key (Optional[str]): API key for the Invariant API. Defaults to the
                                    INVARIANT_API_KEY environment variable.
            timeout_ms (Optional[Union[int, Tuple[int, int]]]): Timeout for API requests
                                    in milliseconds. If it is a single integer, that
                                    value is set as both the connect timeout and the
                                    read timeout value. Otherwise it is a tuple specifying
                                    (connect_timeout, read_timeout). Defaults to
                                    DEFAULT_CONNECTION_TIMEOUT_MS and DEFAULT_READ_TIMEOUT_MS.
            session Optional[Session]: The session to use for requests. If None, a new
                                     session will be created.
        """
        self.api_url = invariant_utils.get_api_url(api_url)
        self.api_key = invariant_utils.get_api_key(api_key)
        self.timeout_ms = (
            (timeout_ms, timeout_ms)
            if isinstance(timeout_ms, int)
            else (
                timeout_ms or (DEFAULT_CONNECTION_TIMEOUT_MS, DEFAULT_READ_TIMEOUT_MS)
            )
        )
        self.session = session if session else requests.Session()
        # Ensure that the session is closed when the program exits.
        atexit.register(_close_session, self.session)

    @property
    def _headers(self) -> Dict[str, str]:
        """
        Generates the headers required for making API requests.

        This property constructs a dictionary containing the necessary headers
        for authorization and content type for API requests.

        Returns:
            Dict[str, str]: A dictionary with the following headers:
                - "Authorization": A Bearer token for API authentication.
                - "Accept": Specifies that the response should be in JSON format.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def __repr__(self) -> str:
        return f"Invariant Client API URL: {self.api_url}"

    def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        pathname: str,
        request_kwargs: Optional[Mapping],
    ) -> requests.Response:
        """
        Makes a request to the Invariant API.

        Args:
            method (Literal["GET", "POST", "PUT", "DELETE"]): The HTTP method to use
                                                              for the request.
            pathname (str): The path to make the request to.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                      the requests method.

        Returns:
            requests.Response: The response from the API.
        """
        request_kwargs = {
            "timeout": (self.timeout_ms[0] / 1000, self.timeout_ms[1] / 1000),
            **request_kwargs,
            "headers": {
                **self._headers,
                **request_kwargs.get("headers", {}),
            },
        }
        try:
            path = self.api_url + pathname
            response = self.session.request(
                method=method,
                url=path,
                stream=False,
                **request_kwargs,
            )
            response.raise_for_status()
            return response
        except requests.ReadTimeout as e:
            raise InvariantAPITimeoutError(
                f"Timeout when calling method: {method} for path: {pathname}."
            ) from e
        except (requests.ConnectionError, requests.ConnectTimeout) as e:
            raise InvariantError(
                f"Connection error when calling method: {method} for path: {pathname}."
            ) from e
        except requests.HTTPError as e:
            if response.status_code == 500:
                raise InvariantAPIError(
                    f"Server error caused failure when calling method: {method} for path: {pathname}."
                ) from e
            if response.status_code == 401:
                raise InvariantAuthError(
                    f"Authentication failed when calling method: {method} for path: {pathname}."
                ) from e
            if response.status_code == 404:
                raise InvariantNotFoundError(
                    f"Resource not found when calling method: {method} for path: {pathname}."
                ) from e
            raise InvariantError(
                f"Error calling method: {method} for path: {pathname}."
            ) from e
        except Exception as e:
            raise InvariantError(
                f"Error calling method: {method} for path: {pathname}."
            ) from e

    def push_trace(
        self,
        request: PushTracesRequest,
        request_kwargs: Optional[Mapping] = None,
    ) -> PushTracesResponse:
        """
        Push trace data to the Invariant API.

        Args:
            request (PushTracesRequest): The request object containing trace data.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                      the requests method.

        Returns:
            PushTracesResponse: The response object.
        """
        if request_kwargs is None:
            request_kwargs = {}
        http_response = self.request(
            method="POST",
            pathname=PUSH_TRACE_API_PATH,
            request_kwargs={
                **request_kwargs,
                "headers": {
                    "Content-Type": "application/json",
                    **request_kwargs.get("headers", {}),
                },
                "json": request.to_json(),
            },
        )
        return PushTracesResponse.from_json(http_response.json())

    def create_request_and_push_trace(
        self,
        messages: List[List[Dict]],
        annotations: Optional[List[List[Dict]]] = None,
        metadata: Optional[List[Dict]] = None,
        dataset: Optional[str] = None,
        request_kwargs: Optional[Mapping] = None,
    ) -> PushTracesResponse:
        """
        Push trace data.

        Args:
            messages (List[List[Dict]]): The messages containing the trace data.
            annotations (Optional[List[List[Dict]]]): The annotations corresponding to the messages.
            metadata (Optional[List[Dict]]): The metadata corresponding to the messages.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                      the requests method.

        Returns:
            PushTracesResponse: The response object.
        """
        if request_kwargs is None:
            request_kwargs = {}
        request = PushTracesRequest(
            messages=messages,
            annotations=(
                AnnotationCreate.from_nested_dicts(annotations) if annotations else None
            ),
            metadata=metadata,
            dataset=dataset,
        )
        return self.push_trace(request, request_kwargs)

    def get_dataset_metadata(
        self,
        dataset_name: str,
        owner_username: str = None,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Get the metadata for a dataset.

        Args:
            dataset_name (str): The name of the dataset to get metadata for.
            owner_username (str): The username of the owner of the dataset. If the caller
                                  is not the owner, this parameter should be set to the
                                  owner's username. If the dataset is not owner by the caller,
                                  this method will return the metadata iff the dataset
                                  is public.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                      the requests method.

        Returns:
            Dict: The response from the API.
        """
        if request_kwargs is None:
            request_kwargs = {}
        pathname = f"{DATASET_METADATA_API_PATH}/{dataset_name}"
        if owner_username:
            pathname += f"?owner_username={owner_username}"
        http_response = self.request(
            method="GET",
            pathname=pathname,
            request_kwargs={
                **request_kwargs,
                "headers": {
                    "Content-Type": "application/json",
                    **request_kwargs.get("headers", {}),
                },
            },
        )
        return http_response.json()

    def update_dataset_metadata(
        self,
        request: UpdateDatasetMetadataRequest,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Update the metadata for a dataset.

        Args:
            request (UpdateDatasetMetadataRequest): The request object containing the dataset name,
                                                    and metadata to update.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                                the requests method.

        Returns:
            Dict: The response from the API.
        """
        if request_kwargs is None:
            request_kwargs = {}
        http_response = self.request(
            method="PUT",
            pathname=f"{DATASET_METADATA_API_PATH}/{request.dataset_name}",
            request_kwargs={
                **request_kwargs,
                "headers": {
                    "Content-Type": "application/json",
                    **request_kwargs.get("headers", {}),
                },
                "json": {
                    "metadata": request.metadata.to_json(),
                    "replace_all": request.replace_all,
                },
            },
        )
        return http_response.json()

    def create_request_and_update_dataset_metadata(
        self,
        dataset_name: str,
        replace_all: bool = False,
        metadata: Optional[Dict] = None,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Update the metadata for a dataset.

        Args:
            dataset_name (str): The name of the dataset to update metadata for.
            metadata (Dict): The metadata to update. The keys should be the metadata fields.
                             Allowed fields are "benchmark", "accuracy", and "name".
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                                the requests method.

        Returns:
            Dict: The response from the API.
        """
        if request_kwargs is None:
            request_kwargs = {}
        metadata = metadata or {}
        request = UpdateDatasetMetadataRequest(
            dataset_name=dataset_name,
            replace_all=replace_all,
            metadata=MetadataUpdate(**metadata),
        )
        return self.update_dataset_metadata(request, request_kwargs)

    def append_messages(
        self,
        request: AppendMessagesRequest,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Append messages to an existing trace.

        Args:
            request (AppendMessagesRequest): The request object containing the trace_id
                                             and messages to append.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                                the requests method.

        Returns:
            Dict: The response from the API.
        """
        if request_kwargs is None:
            request_kwargs = {}
        http_response = self.request(
            method="POST",
            pathname=f"{TRACE_API_PATH}/{request.trace_id}/messages",
            request_kwargs={
                **request_kwargs,
                "headers": {
                    "Content-Type": "application/json",
                    **request_kwargs.get("headers", {}),
                },
                "json": {
                    "messages": request.dump_messages()["messages"],
                },
            },
        )
        return http_response.json()

    def create_request_and_append_messages(
        self,
        messages: List[Dict],
        trace_id: str,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Append messages to an existing trace.

        Args:
            messages (List[Dict]): The messages to append to the trace.
            trace_id (str): The ID of the trace to append messages to.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                                the requests method.

        Returns:
            Dict: The response from the API.
        """
        if request_kwargs is None:
            request_kwargs = {}
        request = AppendMessagesRequest(
            messages=messages,
            trace_id=trace_id,
        )
        return self.append_messages(request, request_kwargs)
