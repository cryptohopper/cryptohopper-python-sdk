"""``client.backtest`` — run and inspect backtests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

BacktestId = int | str


class Backtests:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Start a new backtest. Requires ``manage``. Rate-bucket ``backtest``."""
        return self._client._request("POST", "/backtest/new", json=data)

    def get(self, backtest_id: BacktestId) -> dict[str, Any]:
        """Fetch a backtest. Requires ``read``."""
        return self._client._request(
            "GET", "/backtest/get", params={"backtest_id": backtest_id}
        )

    def list(self, **params: Any) -> list[dict[str, Any]]:
        """List backtests. Requires ``read``."""
        return self._client._request("GET", "/backtest/list", params=params or None)

    def cancel(self, backtest_id: BacktestId) -> dict[str, Any]:
        """Cancel a running backtest. Requires ``manage``."""
        return self._client._request(
            "POST", "/backtest/cancel", json={"backtest_id": backtest_id}
        )

    def restart(self, backtest_id: BacktestId) -> dict[str, Any]:
        """Restart a backtest. Requires ``manage``."""
        return self._client._request(
            "POST", "/backtest/restart", json={"backtest_id": backtest_id}
        )

    def limits(self) -> dict[str, Any]:
        """Current backtest quota. Requires ``read``."""
        return self._client._request("GET", "/backtest/limits")
