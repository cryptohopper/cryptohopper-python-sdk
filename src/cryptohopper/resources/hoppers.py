"""``client.hoppers`` — user trading bots (CRUD, positions, orders, trade, config)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

HopperId = int | str
PositionId = int | str


class Hoppers:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self, *, exchange: str | None = None) -> list[dict[str, Any]]:
        """List the authenticated user's hoppers. Requires ``read``."""
        return self._client._request(
            "GET", "/hopper/list", params={"exchange": exchange}
        )

    def get(self, hopper_id: HopperId) -> dict[str, Any]:
        """Fetch a single hopper. Requires ``read``."""
        return self._client._request(
            "GET", "/hopper/get", params={"hopper_id": hopper_id}
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new hopper. Requires ``manage``."""
        return self._client._request("POST", "/hopper/create", json=data)

    def update(self, hopper_id: HopperId, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing hopper. Requires ``manage``."""
        return self._client._request(
            "POST", "/hopper/update", json={"hopper_id": hopper_id, **data}
        )

    def delete(self, hopper_id: HopperId) -> dict[str, Any]:
        """Delete a hopper. Requires ``manage``."""
        return self._client._request(
            "POST", "/hopper/delete", json={"hopper_id": hopper_id}
        )

    def positions(self, hopper_id: HopperId) -> Sequence[dict[str, Any]]:
        """List open positions for a hopper. Requires ``read``."""
        return self._client._request(
            "GET", "/hopper/positions", params={"hopper_id": hopper_id}
        )

    def position(self, hopper_id: HopperId, position_id: PositionId) -> dict[str, Any]:
        """Fetch a single position. Requires ``read``."""
        return self._client._request(
            "GET",
            "/hopper/position",
            params={"hopper_id": hopper_id, "position_id": position_id},
        )

    def orders(
        self, hopper_id: HopperId, **params: Any
    ) -> Sequence[dict[str, Any]]:
        """List recent orders for a hopper. Requires ``read``."""
        return self._client._request(
            "GET", "/hopper/orders", params={"hopper_id": hopper_id, **params}
        )

    def buy(self, data: dict[str, Any]) -> dict[str, Any]:
        """Place a buy. Requires ``trade``. Subject to the ``order`` rate bucket."""
        return self._client._request("POST", "/hopper/buy", json=data)

    def sell(self, data: dict[str, Any]) -> dict[str, Any]:
        """Place a sell. Requires ``trade``. Subject to the ``order`` rate bucket."""
        return self._client._request("POST", "/hopper/sell", json=data)

    def config_get(self, hopper_id: HopperId) -> dict[str, Any]:
        """Get the full config for a hopper. Requires ``manage``."""
        return self._client._request(
            "GET", "/hopper/configget", params={"hopper_id": hopper_id}
        )

    def config_update(
        self, hopper_id: HopperId, config: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a hopper's config. Requires ``manage``."""
        return self._client._request(
            "POST", "/hopper/configupdate", json={"hopper_id": hopper_id, **config}
        )

    def config_pools(self, hopper_id: HopperId) -> Sequence[dict[str, Any]]:
        """List config pools for a hopper. Requires ``manage``."""
        return self._client._request(
            "GET", "/hopper/configpools", params={"hopper_id": hopper_id}
        )

    def panic(self, hopper_id: HopperId) -> dict[str, Any]:
        """Panic-sell everything. Requires ``trade``."""
        return self._client._request(
            "POST", "/hopper/panic", json={"hopper_id": hopper_id}
        )
