"""Describes the exceptions that can be raised by the Invariant SDK."""


class InvariantError(Exception):
    """An error occurred while communicating with the Invariant API."""


class InvariantAPIError(InvariantError):
    """Internal server error while communicating with Invariant."""


class InvariantUserError(InvariantError):
    """User error caused an exception when communicating with Invariant."""


class InvariantAuthError(InvariantError):
    """Couldn't authenticate with the Invariant API."""


class InvariantNotFoundError(InvariantError):
    """Couldn't find the requested resource."""

class InvariantAPITimeoutError(InvariantError):
    """Request to the Invariant API timed out."""
