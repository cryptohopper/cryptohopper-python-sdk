"""``client.chart`` — saved chart layouts + shared-chart links."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

ChartId = int | str


class Chart:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self) -> Sequence[dict[str, Any]]:
        """List the user's saved charts. Requires ``read``."""
        return self._client._request("GET", "/chart/list")

    def get(self, chart_id: ChartId) -> dict[str, Any]:
        """Fetch a single saved chart. Requires ``read``."""
        return self._client._request(
            "GET", "/chart/get", params={"chart_id": chart_id}
        )

    def save(self, data: dict[str, Any]) -> dict[str, Any]:
        """Save a new chart layout. Requires ``manage``."""
        return self._client._request("POST", "/chart/save", json=data)

    def delete(self, chart_id: ChartId) -> dict[str, Any]:
        """Delete a saved chart. Requires ``manage``."""
        return self._client._request(
            "POST", "/chart/delete", json={"chart_id": chart_id}
        )

    def share_save(self, data: dict[str, Any]) -> dict[str, Any]:
        """Save a shared (public-link) chart. Requires ``manage``."""
        return self._client._request("POST", "/chart/share-save", json=data)

    def share_get(self, share_id: str) -> dict[str, Any]:
        """Fetch a shared chart by its share id / key. Public."""
        return self._client._request(
            "GET", "/chart/share-get", params={"share_id": share_id}
        )
