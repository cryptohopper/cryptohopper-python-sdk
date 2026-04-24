"""``client.tournaments`` — trading competitions."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

TournamentId = int | str


class Tournaments:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self, **params: Any) -> Sequence[dict[str, Any]]:
        """List all tournaments. Requires ``read``."""
        return self._client._request(
            "GET", "/tournaments/gettournaments", params=params or None
        )

    def active(self) -> Sequence[dict[str, Any]]:
        """Currently-active tournaments. Public."""
        return self._client._request("GET", "/tournaments/active")

    def get(self, tournament_id: TournamentId) -> dict[str, Any]:
        """Fetch a single tournament. Requires ``read``."""
        return self._client._request(
            "GET",
            "/tournaments/gettournament",
            params={"tournament_id": tournament_id},
        )

    def search(self, query: str) -> Sequence[dict[str, Any]]:
        """Search across tournaments. Requires ``read``."""
        return self._client._request(
            "GET", "/tournaments/search", params={"q": query}
        )

    def trades(self, tournament_id: TournamentId) -> Sequence[dict[str, Any]]:
        """Trades in a tournament. Requires ``read``."""
        return self._client._request(
            "GET", "/tournaments/trades", params={"tournament_id": tournament_id}
        )

    def stats(self, tournament_id: TournamentId) -> dict[str, Any]:
        """Aggregated stats for a tournament. Requires ``read``."""
        return self._client._request(
            "GET", "/tournaments/stats", params={"tournament_id": tournament_id}
        )

    def activity(self, tournament_id: TournamentId) -> Sequence[dict[str, Any]]:
        """Activity feed for a tournament. Requires ``read``."""
        return self._client._request(
            "GET",
            "/tournaments/activity",
            params={"tournament_id": tournament_id},
        )

    def leaderboard(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Overall cross-tournament leaderboard. Requires ``read``."""
        return self._client._request(
            "GET", "/tournaments/leaderboard", params=params or None
        )

    def tournament_leaderboard(
        self, tournament_id: TournamentId
    ) -> Sequence[dict[str, Any]]:
        """Leaderboard for a specific tournament. Requires ``read``."""
        return self._client._request(
            "GET",
            "/tournaments/leaderboard_tournament",
            params={"tournament_id": tournament_id},
        )

    def join(
        self,
        tournament_id: TournamentId,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Join a tournament. Requires ``manage``."""
        payload = {"tournament_id": tournament_id, **(data or {})}
        return self._client._request("POST", "/tournaments/join", json=payload)

    def leave(self, tournament_id: TournamentId) -> dict[str, Any]:
        """Leave a tournament. Requires ``manage``."""
        return self._client._request(
            "POST", "/tournaments/leave", json={"tournament_id": tournament_id}
        )
