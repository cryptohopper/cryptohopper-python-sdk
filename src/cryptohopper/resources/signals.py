"""``client.signals`` — signal-provider analytics.

Distinct from ``client.market.signals``, which browses marketplace signals
as a consumer.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class Signals:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Signals this provider has published."""
        return self._client._request("GET", "/signals/signals", params=params or None)

    def performance(self, **params: Any) -> dict[str, Any]:
        """Performance stats (winrate, avg profit per signal, etc.)."""
        return self._client._request(
            "GET", "/signals/performance", params=params or None
        )

    def stats(self) -> dict[str, Any]:
        """Overall provider stats."""
        return self._client._request("GET", "/signals/stats")

    def distribution(self) -> dict[str, Any]:
        """Distribution of signals across exchanges / markets / types."""
        return self._client._request("GET", "/signals/distribution")

    def chart_data(self, **params: Any) -> dict[str, Any]:
        """Data series for charting the provider's performance over time."""
        return self._client._request("GET", "/signals/chartdata", params=params or None)
