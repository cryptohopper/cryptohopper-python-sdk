"""``client.exchange`` — public market data (no auth required)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class Exchange:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def ticker(self, *, exchange: str, market: str) -> dict[str, Any]:
        """Current ticker for a market on an exchange."""
        return self._client._request(
            "GET", "/exchange/ticker", params={"exchange": exchange, "market": market}
        )

    def candles(
        self,
        *,
        exchange: str,
        market: str,
        timeframe: str,
        from_: int | None = None,
        to: int | None = None,
    ) -> list[dict[str, Any]]:
        """OHLCV candles. ``timeframe`` e.g. ``"1m"``, ``"1h"``, ``"1d"``."""
        return self._client._request(
            "GET",
            "/exchange/candle",
            params={
                "exchange": exchange,
                "market": market,
                "timeframe": timeframe,
                "from": from_,
                "to": to,
            },
        )

    def orderbook(self, *, exchange: str, market: str) -> dict[str, Any]:
        """Order book depth for a market."""
        return self._client._request(
            "GET", "/exchange/orderbook", params={"exchange": exchange, "market": market}
        )

    def markets(self, exchange: str) -> list[dict[str, Any]]:
        """List markets available on an exchange."""
        return self._client._request(
            "GET", "/exchange/markets", params={"exchange": exchange}
        )

    def currencies(self, exchange: str) -> list[dict[str, Any]]:
        """List currencies available on an exchange."""
        return self._client._request(
            "GET", "/exchange/currencies", params={"exchange": exchange}
        )

    def exchanges(self) -> list[dict[str, Any]]:
        """List all supported exchanges."""
        return self._client._request("GET", "/exchange/exchanges")

    def forex_rates(self) -> dict[str, Any]:
        """Fiat forex rates used for conversion."""
        return self._client._request("GET", "/exchange/forex-rates")
