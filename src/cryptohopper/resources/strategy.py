"""``client.strategy`` — user-defined trading strategies."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

StrategyId = int | str


class Strategies:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self) -> list[dict[str, Any]]:
        """List all strategies owned by the user. Requires ``read``."""
        return self._client._request("GET", "/strategy/strategies")

    def get(self, strategy_id: StrategyId) -> dict[str, Any]:
        """Fetch a strategy. Requires ``read``."""
        return self._client._request(
            "GET", "/strategy/get", params={"strategy_id": strategy_id}
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new strategy. Requires ``manage``."""
        return self._client._request("POST", "/strategy/create", json=data)

    def update(
        self, strategy_id: StrategyId, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Edit an existing strategy. Requires ``manage``."""
        return self._client._request(
            "POST", "/strategy/edit", json={"strategy_id": strategy_id, **data}
        )

    def delete(self, strategy_id: StrategyId) -> dict[str, Any]:
        """Delete a strategy. Requires ``manage``."""
        return self._client._request(
            "POST", "/strategy/delete", json={"strategy_id": strategy_id}
        )
