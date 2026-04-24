"""``client.subscription`` — plans, per-hopper state, credits, billing."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

HopperId = int | str


class Subscription:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def hopper(self, hopper_id: HopperId) -> dict[str, Any]:
        """Subscription state for a specific hopper. Requires ``read``."""
        return self._client._request(
            "GET", "/subscription/hopper", params={"hopper_id": hopper_id}
        )

    def get(self) -> dict[str, Any]:
        """Account-level subscription state. Requires ``read``."""
        return self._client._request("GET", "/subscription/get")

    def plans(self) -> Sequence[dict[str, Any]]:
        """List available subscription plans. Public."""
        return self._client._request("GET", "/subscription/plans")

    def remap(self, data: dict[str, Any]) -> dict[str, Any]:
        """Move a subscription slot from one hopper to another. Requires ``manage``."""
        return self._client._request("POST", "/subscription/remap", json=data)

    def assign(self, data: dict[str, Any]) -> dict[str, Any]:
        """Assign a subscription slot to a hopper. Requires ``manage``."""
        return self._client._request("POST", "/subscription/assign", json=data)

    def get_credits(self) -> dict[str, Any]:
        """Remaining platform credits on the account. Requires ``read``."""
        return self._client._request("GET", "/subscription/getcredits")

    def order_sub(self, data: dict[str, Any]) -> dict[str, Any]:
        """Start a subscription purchase. Requires ``user``."""
        return self._client._request("POST", "/subscription/ordersub", json=data)

    def stop_subscription(
        self, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Cancel / stop an active subscription. Requires ``user``."""
        return self._client._request(
            "POST", "/subscription/stopsubscription", json=data or {}
        )
