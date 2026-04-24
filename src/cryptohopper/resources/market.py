"""``client.market`` — marketplace browse (public, no auth)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

MarketId = int | str


class Market:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def signals(self, **params: Any) -> list[dict[str, Any]]:
        """Browse marketplace signals."""
        return self._client._request("GET", "/market/signals", params=params or None)

    def signal(self, signal_id: MarketId) -> dict[str, Any]:
        """Fetch a single marketplace signal."""
        return self._client._request(
            "GET", "/market/signal", params={"signal_id": signal_id}
        )

    def items(self, **params: Any) -> list[dict[str, Any]]:
        """Browse marketplace items (strategies, templates, signals)."""
        return self._client._request(
            "GET", "/market/marketitems", params=params or None
        )

    def item(self, item_id: MarketId) -> dict[str, Any]:
        """Fetch a single marketplace item."""
        return self._client._request(
            "GET", "/market/marketitem", params={"item_id": item_id}
        )

    def homepage(self) -> dict[str, Any]:
        """Marketplace homepage."""
        return self._client._request("GET", "/market/homepage")
