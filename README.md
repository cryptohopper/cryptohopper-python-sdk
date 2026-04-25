# cryptohopper

[![PyPI](https://img.shields.io/pypi/v/cryptohopper?logo=pypi&logoColor=white&include_prereleases)](https://pypi.org/project/cryptohopper/)
[![PyPI downloads](https://img.shields.io/pypi/dm/cryptohopper?logo=pypi&logoColor=white&label=downloads)](https://pypi.org/project/cryptohopper/)
[![Python versions](https://img.shields.io/pypi/pyversions/cryptohopper?logo=python&logoColor=white)](https://pypi.org/project/cryptohopper/)
[![CI](https://github.com/cryptohopper/cryptohopper-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/cryptohopper/cryptohopper-python-sdk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/pypi/l/cryptohopper?color=blue)](LICENSE)

Official Python SDK for the [Cryptohopper](https://www.cryptohopper.com) API.

> **Status: 0.4.0a1** — full coverage of all 18 public API domains: `user`, `hoppers`, `exchange`, `strategy`, `backtest`, `market`, `signals`, `arbitrage`, `marketmaker`, `template`, `ai`, `platform`, `chart`, `subscription`, `social`, `tournaments`, `webhooks`, `app`.

**Deeper docs:** [Getting Started](docs/Getting-Started.md) · [Authentication](docs/Authentication.md) · [Error Handling](docs/Error-Handling.md) · [Rate Limits](docs/Rate-Limits.md)

## Install

```bash
pip install cryptohopper
```

Requires Python 3.10+.

## Quickstart

```python
import os
from cryptohopper import CryptohopperClient

with CryptohopperClient(api_key=os.environ["CRYPTOHOPPER_TOKEN"]) as ch:
    me = ch.user.get()
    print(me["email"])

    ticker = ch.exchange.ticker(exchange="binance", market="BTC/USDT")
    print(ticker["last"])
```

## Authentication

Cryptohopper uses OAuth2 bearer tokens. To get one:

1. Sign in at [cryptohopper.com](https://www.cryptohopper.com) and open the developer dashboard.
2. Create an OAuth application — you'll receive a `client_id` and `client_secret`.
3. Drive the OAuth consent flow (`/oauth-consent?app_id=<client_id>&redirect_uri=<your_uri>&state=<csrf>`) to receive a 40-character bearer token scoped to the permissions you requested.

Pass the token as `api_key`. Optionally pass your OAuth `client_id` as `app_key` — it's sent as the `x-api-app-key` header.

```python
ch = CryptohopperClient(
    api_key=os.environ["CRYPTOHOPPER_TOKEN"],
    app_key=os.environ.get("CRYPTOHOPPER_CLIENT_ID"),  # optional
)
```

## Resources

```python
# User
ch.user.get()

# Hoppers
ch.hoppers.list(exchange="binance")
ch.hoppers.get(42)
ch.hoppers.create({"name": "My Bot", "exchange": "binance"})
ch.hoppers.update(42, {"name": "Renamed"})
ch.hoppers.delete(42)
ch.hoppers.positions(42)
ch.hoppers.orders(42)
ch.hoppers.buy({"hopper_id": 42, "market": "BTC/USDT", "amount": 0.001})
ch.hoppers.sell({"hopper_id": 42, "market": "BTC/USDT", "amount": 0.001})
ch.hoppers.config_get(42)
ch.hoppers.config_update(42, {"strategy_id": 99})
ch.hoppers.panic(42)

# Exchange (public — no auth required)
ch.exchange.ticker(exchange="binance", market="BTC/USDT")
ch.exchange.candles(exchange="binance", market="BTC/USDT", timeframe="1h")
ch.exchange.orderbook(exchange="binance", market="BTC/USDT")
ch.exchange.markets("binance")
ch.exchange.exchanges()

# Strategy
ch.strategy.list()
ch.strategy.get(5)
ch.strategy.create({"name": "My Strategy"})
ch.strategy.update(5, {"name": "Renamed"})
ch.strategy.delete(5)

# Backtest
ch.backtest.create({"hopper_id": 42, "from_date": "2026-01-01", "to_date": "2026-03-01"})
ch.backtest.get(1)
ch.backtest.list()
ch.backtest.cancel(1)
ch.backtest.limits()

# Marketplace (public — no auth required)
ch.market.signals(type="buy")
ch.market.signal(99)
ch.market.items(type="strategy")
ch.market.homepage()
```

## Client options

| Option | Default | Description |
|---|---|---|
| `api_key` | — (required) | OAuth2 bearer token |
| `app_key` | — | Optional OAuth `client_id`, sent as `x-api-app-key` |
| `base_url` | `https://api.cryptohopper.com/v1` | Override for staging/dev |
| `timeout` | `30.0` | Per-request timeout in seconds |
| `max_retries` | `3` | Retries on HTTP 429 (respects `Retry-After`). Set to `0` to disable. |
| `user_agent` | — | Appended after `cryptohopper-sdk-python/<version>` |
| `http_client` | — | Inject a custom `httpx.Client` |

## Errors

Every non-2xx response becomes a `CryptohopperError`:

```python
from cryptohopper import CryptohopperClient, CryptohopperError

try:
    ch.user.get()
except CryptohopperError as err:
    print(err.code)            # "UNAUTHORIZED" | "FORBIDDEN" | "RATE_LIMITED" | ...
    print(err.status)          # HTTP status
    print(err.server_code)     # Numeric unique error code from the server, if any
    print(err.ip_address)      # Client IP the server saw (IP-whitelist debug help)
    print(err.retry_after_ms)  # Milliseconds to wait on 429 (if server sent Retry-After)
```

Unknown server-side codes pass through as-is on `.code`.

## Rate limiting

The server enforces three buckets (`normal` 30/min, `order` 8/8s, `backtest` 1/2s). On HTTP 429 the SDK retries with exponential backoff up to `max_retries` (default 3), respecting `Retry-After`. Pass `max_retries=0` to disable auto-retry.

## Development

```bash
pip install -e ".[dev]"
ruff check .
mypy src
pytest -q
```

## Release

Push a `py-v<version>` git tag. The release workflow runs ruff + mypy + pytest, verifies tag-version parity, builds sdist + wheel, and publishes via **PyPI Trusted Publishing (OIDC)** — no long-lived API token needed. Configure the publisher at [pypi.org/manage/account/publishing](https://pypi.org/manage/account/publishing/) before the first release.

## License

MIT — see [LICENSE](./LICENSE).
