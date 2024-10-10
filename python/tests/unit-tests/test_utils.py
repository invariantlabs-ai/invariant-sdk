"""Unit tests for the utility functions in `utils.py`."""

from unittest.mock import patch

import invariant.utils as invariant_utils
from invariant.types.exceptions import InvariantUserError
import pytest


def test_get_api_key() -> None:
    """Test the `get_api_key` function."""
    assert invariant_utils.get_api_key("provided_api_key") == "provided_api_key"

    with patch.dict("os.environ", {"INVARIANT_API_KEY": "env_api_key"}, clear=True):
        assert invariant_utils.get_api_key(None) == "env_api_key"

    with pytest.raises(InvariantUserError):
        with patch.dict("os.environ", {}, clear=True):
            assert invariant_utils.get_api_key(None) is None


def test_get_api_url() -> None:
    """Test the `get_api_url` function."""
    assert invariant_utils.get_api_url("http://provided.url") == "http://provided.url"

    with patch.dict("os.environ", {"INVARIANT_API_ENDPOINT": "http://env.url"}):
        assert invariant_utils.get_api_url(None) == "http://env.url"

    with patch.dict("os.environ", {}, clear=True):
        assert invariant_utils.get_api_url(None) == "https://explorer.invariantlabs.ai"

    with patch.dict(
        "os.environ",
        {"INVARIANT_API_ENDPOINT": "https://some-other-env-explorer.invariantlabs.ai"},
    ):
        assert (
            invariant_utils.get_api_url(None)
            == "https://some-other-env-explorer.invariantlabs.ai"
        )

    with pytest.raises(InvariantUserError):
        invariant_utils.get_api_url(" ")
