"""CryptohopperClient — the public entry point.

Holds the OAuth2 bearer token (+ optional ``app_key``) and exposes
namespaced resources (``client.hoppers``, ``client.exchange``, ...).
The internal transport is a thin wrapper around ``httpx.Client`` that
parses the Cryptohopper error envelope (``{status, code, error, message,
ip_address}``) and auto-retries 429s honouring ``Retry-After``.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Literal

import httpx

from ._version import CURRENT_VERSION
from .errors import CryptohopperError

DEFAULT_BASE_URL = "https://api.cryptohopper.com/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

HttpMethod = Literal["GET", "POST", "PATCH", "DELETE", "PUT"]

if TYPE_CHECKING:
    from .resources.ai import AI
    from .resources.arbitrage import Arbitrage
    from .resources.backtest import Backtests
    from .resources.chart import Chart
    from .resources.exchange import Exchange
    from .resources.hoppers import Hoppers
    from .resources.market import Market
    from .resources.marketmaker import MarketMaker
    from .resources.platform import Platform
    from .resources.signals import Signals
    from .resources.strategy import Strategies
    from .resources.subscription import Subscription
    from .resources.template import Templates
    from .resources.user import User


class CryptohopperClient:
    """Synchronous Cryptohopper API client.

    Example::

        from cryptohopper import CryptohopperClient

        with CryptohopperClient(api_key="ch_...") as ch:
            me = ch.user.get()
            ticker = ch.exchange.ticker(exchange="binance", market="BTC/USDT")

    Args:
        api_key: 40-char OAuth2 bearer token. Required.
        app_key: Optional OAuth ``client_id``, sent as ``x-api-app-key``.
        base_url: Override for staging. Defaults to
            ``https://api.cryptohopper.com/v1``.
        timeout: Per-request timeout in seconds. Defaults to 30.
        max_retries: Retries on HTTP 429 (respects ``Retry-After``).
            Set to ``0`` to disable. Defaults to 3.
        user_agent: Appended after ``cryptohopper-sdk-python/<v>``.
        http_client: Bring-your-own ``httpx.Client`` (for proxies, etc.).
    """

    base_url: str
    hoppers: Hoppers
    exchange: Exchange
    strategy: Strategies
    backtest: Backtests
    market: Market
    user: User
    signals: Signals
    arbitrage: Arbitrage
    marketmaker: MarketMaker
    template: Templates
    ai: AI
    platform: Platform
    chart: Chart
    subscription: Subscription

    def __init__(
        self,
        *,
        api_key: str,
        app_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        user_agent: str | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if not api_key:
            raise TypeError("CryptohopperClient: `api_key` is required")
        self._api_key = api_key
        self._app_key = app_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._user_agent_suffix = user_agent
        self._http = http_client or httpx.Client(timeout=timeout)
        self._owns_http = http_client is None

        # Import here to avoid a circular at module import time.
        from .resources.ai import AI
        from .resources.arbitrage import Arbitrage
        from .resources.backtest import Backtests
        from .resources.chart import Chart
        from .resources.exchange import Exchange
        from .resources.hoppers import Hoppers
        from .resources.market import Market
        from .resources.marketmaker import MarketMaker
        from .resources.platform import Platform
        from .resources.signals import Signals
        from .resources.strategy import Strategies
        from .resources.subscription import Subscription
        from .resources.template import Templates
        from .resources.user import User

        self.user = User(self)
        self.hoppers = Hoppers(self)
        self.exchange = Exchange(self)
        self.strategy = Strategies(self)
        self.backtest = Backtests(self)
        self.market = Market(self)
        self.signals = Signals(self)
        self.arbitrage = Arbitrage(self)
        self.marketmaker = MarketMaker(self)
        self.template = Templates(self)
        self.ai = AI(self)
        self.platform = Platform(self)
        self.chart = Chart(self)
        self.subscription = Subscription(self)

    def __enter__(self) -> CryptohopperClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client (if we own it)."""
        if self._owns_http:
            self._http.close()

    def _user_agent(self) -> str:
        if self._user_agent_suffix:
            return f"cryptohopper-sdk-python/{CURRENT_VERSION} {self._user_agent_suffix}"
        return f"cryptohopper-sdk-python/{CURRENT_VERSION}"

    def _request(
        self,
        method: HttpMethod,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Any:
        """Internal transport. Resources call this; users shouldn't."""
        retries = max_retries if max_retries is not None else self._max_retries
        attempt = 0
        while True:
            try:
                return self._do_request(
                    method, path, json=json, params=params, timeout=timeout
                )
            except CryptohopperError as err:
                if err.code == "RATE_LIMITED" and attempt < retries:
                    wait_ms = err.retry_after_ms if err.retry_after_ms is not None else 1000 * 2**attempt
                    time.sleep(wait_ms / 1000.0)
                    attempt += 1
                    continue
                raise

    def _do_request(
        self,
        method: HttpMethod,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> Any:
        url = f"{self.base_url}{path if path.startswith('/') else '/' + path}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "User-Agent": self._user_agent(),
            "Accept": "application/json",
        }
        if self._app_key:
            headers["x-api-app-key"] = self._app_key

        clean_params: dict[str, Any] | None = None
        if params is not None:
            clean_params = {k: v for k, v in params.items() if v is not None}
            if not clean_params:
                clean_params = None

        try:
            resp = self._http.request(
                method,
                url,
                json=json if json is not None else None,
                params=clean_params,
                headers=headers,
                timeout=timeout if timeout is not None else self._timeout,
            )
        except httpx.TimeoutException as err:
            raise CryptohopperError(
                code="TIMEOUT",
                message=f"Request timed out ({err})",
                status=0,
            ) from err
        except httpx.HTTPError as err:
            raise CryptohopperError(
                code="NETWORK_ERROR",
                message=f"Could not reach {self.base_url} ({err})",
                status=0,
            ) from err

        parsed: Any = None
        text = resp.text
        if text:
            try:
                parsed = resp.json()
            except ValueError:
                parsed = None

        if resp.status_code >= 400:
            body = parsed if isinstance(parsed, dict) else {}
            message = body.get("message") or f"Request failed ({resp.status_code})"
            raw_code = body.get("code")
            server_code = raw_code if isinstance(raw_code, int) and raw_code > 0 else None
            ip_address = body.get("ip_address") if isinstance(body.get("ip_address"), str) else None
            retry_after_ms = _parse_retry_after(resp.headers.get("retry-after"))
            raise CryptohopperError(
                code=_default_code_for_status(resp.status_code),
                message=message,
                status=resp.status_code,
                server_code=server_code,
                ip_address=ip_address,
                retry_after_ms=retry_after_ms,
            )

        if isinstance(parsed, dict) and "data" in parsed:
            return parsed["data"]
        return parsed


def _default_code_for_status(status: int) -> str:
    if status == 400:
        return "VALIDATION_ERROR"
    if status == 401:
        return "UNAUTHORIZED"
    if status == 402:
        return "DEVICE_UNAUTHORIZED"
    if status == 403:
        return "FORBIDDEN"
    if status == 404:
        return "NOT_FOUND"
    if status == 409:
        return "CONFLICT"
    if status == 422:
        return "VALIDATION_ERROR"
    if status == 429:
        return "RATE_LIMITED"
    if status == 503:
        return "SERVICE_UNAVAILABLE"
    if status >= 500:
        return "SERVER_ERROR"
    return "UNKNOWN"


def _parse_retry_after(header: str | None) -> int | None:
    """Parse an RFC 7231 ``Retry-After`` header as milliseconds."""
    if header is None:
        return None
    try:
        seconds = float(header)
    except ValueError:
        pass
    else:
        if seconds < 0:
            return None
        return round(seconds * 1000)

    from datetime import datetime, timezone
    from email.utils import parsedate_to_datetime

    try:
        when = parsedate_to_datetime(header)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    delta_ms = round((when - datetime.now(timezone.utc)).total_seconds() * 1000)
    return max(delta_ms, 0)
