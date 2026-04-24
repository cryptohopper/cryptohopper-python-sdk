"""``client.marketmaker`` — market-maker bot ops + market-trend overrides + backlog."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

BacklogId = int | str


class MarketMaker:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def get(self, **params: Any) -> dict[str, Any]:
        """Fetch the market-maker state for a hopper. Requires ``read``."""
        return self._client._request("GET", "/marketmaker/get", params=params or None)

    def cancel(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancel running market-maker orders. Requires ``trade``."""
        return self._client._request("POST", "/marketmaker/cancel", json=data or {})

    def history(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Historical order activity. Requires ``read``."""
        return self._client._request(
            "GET", "/marketmaker/history", params=params or None
        )

    # ─── Market-trend overrides ──────────────────────────────────────────

    def get_market_trend(self, **params: Any) -> dict[str, Any]:
        """Read the current market-trend override. Requires ``read``."""
        return self._client._request(
            "GET", "/marketmaker/get-market-trend", params=params or None
        )

    def set_market_trend(self, data: dict[str, Any]) -> dict[str, Any]:
        """Set a market-trend override. Requires ``manage``."""
        return self._client._request(
            "POST", "/marketmaker/set-market-trend", json=data
        )

    def delete_market_trend(
        self, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Remove the current market-trend override. Requires ``manage``."""
        return self._client._request(
            "POST", "/marketmaker/delete-market-trend", json=data or {}
        )

    # ─── Backlog ─────────────────────────────────────────────────────────

    def backlogs(self, **params: Any) -> Sequence[dict[str, Any]]:
        """List queued/pending market-maker backlog items. Requires ``read``."""
        return self._client._request(
            "GET", "/marketmaker/get-backlogs", params=params or None
        )

    def backlog(self, backlog_id: BacklogId) -> dict[str, Any]:
        """Fetch a single backlog item. Requires ``read``."""
        return self._client._request(
            "GET", "/marketmaker/get-backlog", params={"backlog_id": backlog_id}
        )

    def delete_backlog(self, backlog_id: BacklogId) -> dict[str, Any]:
        """Delete a backlog item. Requires ``manage``."""
        return self._client._request(
            "POST", "/marketmaker/delete-backlog", json={"backlog_id": backlog_id}
        )
