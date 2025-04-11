"""Client for interacting with the Invariant APIs."""

import atexit
from typing import Dict, List, Literal, Mapping, Optional, Tuple, Union
from invariant_sdk.types.annotations import AnnotationCreate
from invariant_sdk.types.exceptions import (
    InvariantError,
    InvariantAPITimeoutError,
)
from invariant_sdk.types.push_traces import PushTracesRequest, PushTracesResponse
from invariant_sdk.types.update_dataset_metadata import (
    MetadataUpdate,
    UpdateDatasetMetadataRequest,
)
from invariant_sdk.types.append_messages import AppendMessagesRequest
from invariant_sdk.base_client import (
    BaseClient,
    PUSH_TRACE_API_PATH,
    DATASET_METADATA_API_PATH,
    TRACE_API_PATH,
)

import requests
import urllib3


def _close_session(session: requests.Session) -> None:
    session.close()


class Client(BaseClient):
    """Client for interacting with the Invariant APIs."""

    __slots__ = ["session"]

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_ms: Optional[Union[int, Tuple[int, int]]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        super().__init__(api_url, api_key, timeout_ms)
        self.session = session if session else requests.Session()
        atexit.register(_close_session, self.session)

    def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        pathname: str,
        request_kwargs: Optional[Mapping] = None,
    ) -> requests.Response:
        """
        Makes a request to the Invariant API.

        Args:
            method (Literal["GET", "POST", "PUT", "DELETE"]): The HTTP method to use.
            pathname (str): The path to make the request to.
            request_kwargs (Optional[Mapping]): Additional keyword arguments for the request.

        Returns:
            requests.Response: The response from the API.
        """
        request_kwargs = self._prepare_request_kwargs(request_kwargs)
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
                f"Timeout when calling method: {method} for path: {pathname}. Server took too long."
            ) from e
        except requests.ConnectTimeout as e:
            raise InvariantAPITimeoutError(
                f"Timeout when connecting to server for method: {method} on path: {pathname}."
            ) from e
        except requests.ConnectionError as e:
            cause = getattr(e, "__cause__", None)
            if isinstance(cause, TimeoutError):
                raise InvariantAPITimeoutError(
                    f"Timeout when calling method: {method} for path: {pathname}."
                ) from e
            if isinstance(cause, urllib3.exceptions.ProtocolError):
                inner_cause = getattr(cause, "__cause__", None)
                if isinstance(inner_cause, TimeoutError):
                    raise InvariantAPITimeoutError(
                        f"Timeout when calling method: {method} for path: {pathname}."
                    ) from e
            raise InvariantError(
                f"Connection error when calling method: {method} for path: {pathname}."
            ) from e
        except requests.HTTPError as e:
            response = e.response
            if response is not None:
                self._handle_http_error(method, pathname, response)
        except Exception as e:
            raise InvariantError(
                f"Unexpected error ({type(e).__name__}): {e} when calling method: {method} for path: {pathname}."
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
        request_kwargs = self._prepare_push_trace_request(request, request_kwargs)
        http_response = self.request(
            method="POST",
            pathname=PUSH_TRACE_API_PATH,
            request_kwargs=request_kwargs,
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
        pathname = f"{DATASET_METADATA_API_PATH}/{dataset_name}"
        if owner_username:
            pathname += f"?owner_username={owner_username}"
        http_response = self.request(
            method="GET",
            pathname=pathname,
            request_kwargs=self._prepare_get_dataset_metadata_request(request_kwargs),
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
        request_kwargs = self._prepare_update_dataset_metadata_request(
            request, request_kwargs
        )
        http_response = self.request(
            method="PUT",
            pathname=f"{DATASET_METADATA_API_PATH}/{request.dataset_name}",
            request_kwargs=request_kwargs,
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
        request_kwargs = self._prepare_append_messages_request(request, request_kwargs)
        http_response = self.request(
            method="POST",
            pathname=f"{TRACE_API_PATH}/{request.trace_id}/messages",
            request_kwargs=request_kwargs,
        )
        return http_response.json()

    def create_request_and_append_messages(
        self,
        messages: List[Dict],
        trace_id: str,
        annotations: Optional[List[Dict]] = None,
        request_kwargs: Optional[Mapping] = None,
    ) -> Dict:
        """
        Append messages to an existing trace.

        Args:
            messages (List[Dict]): The messages to append to the trace.
            trace_id (str): The ID of the trace to append messages to.
            annotations (Optional[List[Dict]]): The annotations corresponding to the messages.
            request_kwargs (Optional[Mapping]): Additional keyword arguments to pass to
                                                the requests method.

        Returns:
            Dict: The response from the API.
        """
        request = AppendMessagesRequest(
            trace_id=trace_id,
            messages=messages,
            annotations=(
                AnnotationCreate.from_dicts(annotations) if annotations else None
            ),
        )
        return self.append_messages(request, request_kwargs)
