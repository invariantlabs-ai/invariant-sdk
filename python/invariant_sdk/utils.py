"""Utility functions for the Invariant SDK."""

import os
from typing import Optional, cast

from invariant_sdk.types.exceptions import InvariantUserError

DEFAULT_INVARIANT_API_URL = "https://explorer.invariantlabs.ai"


def fetch_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieve an environment variable's value.

    This function attempts to get the value of the environment variable specified by `name`.
    If the environment variable is not set, it returns the provided `default` value.

    Args:
        name (str): The name of the environment variable to retrieve.
        default (Optional[str]): The value to return if the environment variable is not set.
                                 Defaults to None.

    Returns:
        Optional[str]: The value of the environment variable, or the `default` value if the
                       environment variable is not set.
    """
    value = os.environ.get(name)
    return value if value is not None else default


def get_api_url(api_url: Optional[str]) -> str:
    """
    Retrieve the API url from the provided value or from the environment variable.

    Args:
        api_url (Optional[str]): The API url provided as an argument. If None, the
                                 function will attempt to fetch it from the environment.

    Returns:
        str: The API url, stripped of any leading or trailing whitespace.

    Raises:
        InvariantUserError: If the API url is empty or contains only whitespace.
    """
    _api_url = api_url or cast(
        str,
        fetch_env_var(
            "INVARIANT_API_ENDPOINT",
            default=DEFAULT_INVARIANT_API_URL,
        ),
    )
    if not _api_url.strip():
        raise InvariantUserError("Invariant API URL cannot be empty")
    return _api_url.strip()


def get_api_key(api_key: Optional[str]) -> str:
    """
    Retrieve the API key from the provided value or from the environment variable.

    Args:
        api_key (Optional[str]): The API key provided as an argument. If None, the
                                 function will attempt to fetch it from the environment.

    Returns:
        str: The API key, stripped of any leading or trailing whitespace.

    Raises:
        InvariantUserError: If the API key is empty or contains only whitespace.
    """
    _api_key = api_key or fetch_env_var("INVARIANT_API_KEY", default=None)
    if not _api_key or not _api_key.strip():
        raise InvariantUserError("Invariant API key cannot be empty")
    return _api_key.strip()
