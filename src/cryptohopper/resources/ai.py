"""``client.ai`` — AI assistant: credits + LLM analysis."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient


class AI:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self, **params: Any) -> Sequence[dict[str, Any]]:
        """List AI assistant items / sessions. Requires ``read``."""
        return self._client._request("GET", "/ai/list", params=params or None)

    def get(self, id: int | str) -> dict[str, Any]:
        """Fetch a single AI item / session. Requires ``read``."""
        return self._client._request("GET", "/ai/get", params={"id": id})

    def available_models(self) -> Sequence[dict[str, Any]]:
        """Models available to the authenticated user."""
        return self._client._request("GET", "/ai/availablemodels")

    # ─── Credits ─────────────────────────────────────────────────────────

    def get_credits(self) -> dict[str, Any]:
        """Remaining AI credit balance. Requires ``read``."""
        return self._client._request("GET", "/ai/getaicredits")

    def credit_invoices(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Past invoices for AI-credit purchases. Requires ``read``."""
        return self._client._request(
            "GET", "/ai/aicreditinvoices", params=params or None
        )

    def credit_transactions(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Credit spend/top-up transaction history. Requires ``read``."""
        return self._client._request(
            "GET", "/ai/aicredittransactions", params=params or None
        )

    def buy_credits(self, data: dict[str, Any]) -> dict[str, Any]:
        """Start a purchase of additional credits. Requires ``user``."""
        return self._client._request("POST", "/ai/buyaicredits", json=data)

    # ─── LLM analysis ────────────────────────────────────────────────────

    def llm_analyze_options(self) -> dict[str, Any]:
        """Options/metadata for the LLM analyse endpoint. Requires ``read``."""
        return self._client._request("GET", "/ai/aillmanalyzeoptions")

    def llm_analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        """Run an LLM analysis. Usually async — returns a job id. Requires ``manage``."""
        return self._client._request("POST", "/ai/doaillmanalyze", json=data)

    def llm_analyze_results(self, **params: Any) -> dict[str, Any]:
        """Fetch the result(s) of an LLM analysis. Requires ``read``."""
        return self._client._request(
            "GET", "/ai/aillmanalyzeresults", params=params or None
        )

    def llm_results(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Historical LLM analysis results. Requires ``read``."""
        return self._client._request(
            "GET", "/ai/aillmresults", params=params or None
        )
