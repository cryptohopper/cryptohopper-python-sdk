"""``client.platform`` — marketing / i18n / discovery reads (all public)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class Platform:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def latest_blog(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Latest blog posts. Public."""
        return self._client._request(
            "GET", "/platform/latestblog", params=params or None
        )

    def documentation(self, **params: Any) -> dict[str, Any]:
        """Documentation articles. Public."""
        return self._client._request(
            "GET", "/platform/documentation", params=params or None
        )

    def promo_bar(self) -> dict[str, Any]:
        """Active promo bar content. Public."""
        return self._client._request("GET", "/platform/promobar")

    def search_documentation(self, query: str) -> Sequence[dict[str, Any]]:
        """Full-text search across public documentation. Public."""
        return self._client._request(
            "GET", "/platform/searchdocumentation", params={"q": query}
        )

    def countries(self) -> Sequence[dict[str, Any]]:
        """Full list of countries (ISO codes + display names). Public."""
        return self._client._request("GET", "/platform/countries")

    def country_allowlist(self) -> Sequence[dict[str, Any]]:
        """Countries the platform currently allows. Public."""
        return self._client._request("GET", "/platform/countryallowlist")

    def ip_country(self) -> dict[str, Any]:
        """Country resolved from the caller's IP. Public."""
        return self._client._request("GET", "/platform/ipcountry")

    def languages(self) -> Sequence[dict[str, Any]]:
        """Supported UI languages. Public."""
        return self._client._request("GET", "/platform/languages")

    def bot_types(self) -> Sequence[dict[str, Any]]:
        """Enumeration of available bot types. Public."""
        return self._client._request("GET", "/platform/bottypes")
