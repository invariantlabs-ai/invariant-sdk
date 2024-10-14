"""Client for interacting with the Invariant APIs."""

import atexit
import weakref
from typing import Dict, Literal, Mapping, Optional, Tuple, Union
from invariant.types.exceptions import (
    InvariantError,
    InvariantAPITimeoutError,
    InvariantAPIError,
    InvariantAuthError,
    InvariantNotFoundError,
)
from invariant.types.push_traces import PushTracesRequest, PushTracesResponse

import requests
import invariant.utils as invariant_utils

DEFAULT_CONNECTION_TIMEOUT_MS = 5_000
DEFAULT_READ_TIMEOUT_MS = 20_000
PUSH_TRACE_API_PATH = "/api/v1/push/trace"


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
        request_kwargs: Optional[Mapping] = None,
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

    def push_trace(self, request: PushTracesRequest) -> PushTracesResponse:
        """
        Push trace data to the Invariant API.

        Args:
            request (PushTracesRequest): The request object containing trace data.

        Returns:
            PushTracesResponse: The response object.
        """
        http_response = self.request(
            method="POST",
            pathname=PUSH_TRACE_API_PATH,
            request_kwargs={
                "json": request.to_json(),
                "headers": {"Content-Type": "application/json"},
            },
        )
        return PushTracesResponse.from_json(http_response.json())
