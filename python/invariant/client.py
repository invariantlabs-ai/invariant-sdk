"""Client for interacting with the Invariant APIs."""

from typing import Optional

import utils as invariant_utils


class Client:
    """Client for interacting with the Invariant APIs."""

    __slots__ = ["api_url", "api_key"]

    def __init__(
        self, api_url: Optional[str] = None, api_key: Optional[str] = None
    ) -> None:
        """
        Initialize a Client instance.

        Args:
            api_url (Optional[str]): URL for the Invariant API. Defaults to the
                                     INVARIANT_API_ENDPOINT environment variable or
                                     https://explorer.invariantlabs.ai if not set.
            api_key (Optional[str]): API key for the Invariant API. Defaults to the
                                     INVARIANT_API_KEY environment variable.
        """
        self.api_url = invariant_utils.get_api_url(api_url)
        self.api_key = invariant_utils.get_api_key(api_key)
