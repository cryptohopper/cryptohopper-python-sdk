"""``client.user`` — authenticated user profile."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class User:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def get(self) -> dict[str, Any]:
        """Fetch the authenticated user's profile. Requires ``user`` scope."""
        return self._client._request("GET", "/user/get")
