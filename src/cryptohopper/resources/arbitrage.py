"""``client.arbitrage`` — exchange + market arbitrage operations.

Two distinct flavours:
  • ``exchange_*`` — cross-exchange arbitrage.
  • ``market_*``   — intra-exchange market arbitrage.
Plus a shared backlog API.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

BacklogId = int | str


class Arbitrage:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    # ─── Cross-exchange arbitrage ─────────────────────────────────────────

    def exchange_start(self, data: dict[str, Any]) -> dict[str, Any]:
        """Start a cross-exchange arbitrage run. Requires ``trade``."""
        return self._client._request("POST", "/arbitrage/exchange", json=data)

    def exchange_cancel(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancel a cross-exchange arbitrage run. Requires ``trade``."""
        return self._client._request("POST", "/arbitrage/cancel", json=data or {})

    def exchange_results(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Fetch results of exchange-arbitrage runs. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/results", params=params or None
        )

    def exchange_history(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Historical exchange-arbitrage runs. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/history", params=params or None
        )

    def exchange_total(self) -> dict[str, Any]:
        """Running totals across exchange-arbitrage runs. Requires ``read``."""
        return self._client._request("GET", "/arbitrage/total")

    def exchange_reset_total(self) -> dict[str, Any]:
        """Reset the running totals. Requires ``manage``."""
        return self._client._request("POST", "/arbitrage/resettotal", json={})

    # ─── Intra-exchange market arbitrage ──────────────────────────────────

    def market_start(self, data: dict[str, Any]) -> dict[str, Any]:
        """Start an intra-exchange arbitrage run. Requires ``trade``."""
        return self._client._request("POST", "/arbitrage/market", json=data)

    def market_cancel(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancel a market-arbitrage run. Requires ``trade``."""
        return self._client._request("POST", "/arbitrage/market-cancel", json=data or {})

    def market_result(self, **params: Any) -> dict[str, Any]:
        """Result of a specific market-arbitrage run. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/market-result", params=params or None
        )

    def market_history(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Historical market-arb runs. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/market-history", params=params or None
        )

    # ─── Backlog (shared) ────────────────────────────────────────────────

    def backlogs(self, **params: Any) -> Sequence[dict[str, Any]]:
        """List queued/pending backlog items. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/get-backlogs", params=params or None
        )

    def backlog(self, backlog_id: BacklogId) -> dict[str, Any]:
        """Fetch a single backlog item. Requires ``read``."""
        return self._client._request(
            "GET", "/arbitrage/get-backlog", params={"backlog_id": backlog_id}
        )

    def delete_backlog(self, backlog_id: BacklogId) -> dict[str, Any]:
        """Delete a backlog item. Requires ``manage``."""
        return self._client._request(
            "POST", "/arbitrage/delete-backlog", json={"backlog_id": backlog_id}
        )
