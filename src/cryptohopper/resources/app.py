"""``client.app`` — mobile app store receipts + in-app purchases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class App:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def receipt(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate an App Store / Play Store receipt."""
        return self._client._request("POST", "/app/receipt", json=data)

    def in_app_purchase(self, data: dict[str, Any]) -> dict[str, Any]:
        """Record an in-app purchase."""
        return self._client._request("POST", "/app/in_app_purchase", json=data)
