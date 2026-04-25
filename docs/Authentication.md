# Authentication

Every SDK request (except a handful of public endpoints like `/exchange/ticker`, `/market/homepage`, and `/platform/*`) requires an OAuth2 bearer token:

```
Authorization: Bearer <40-char token>
```

## Obtaining a token

1. Log in to [cryptohopper.com](https://www.cryptohopper.com).
2. Developer → Create App — gives you a `client_id` + `client_secret`.
3. Complete the OAuth consent flow for your app, which returns a bearer token.

Options to automate step 3:

- **The official CLI**: `cryptohopper login` opens the consent page, runs a loopback listener, and persists the token to `~/.cryptohopper/config.json`. You can read the token from there or run the CLI and the SDK side-by-side.
- **Your own code**: call the server's `/oauth2/authorize` + `/oauth2/token` endpoints directly. The CLI's implementation is small (~300 lines) and a reasonable reference.

## Client construction

```python
import os
from cryptohopper import CryptohopperClient

ch = CryptohopperClient(
    api_key=os.environ["CRYPTOHOPPER_TOKEN"],
    app_key=os.environ.get("CRYPTOHOPPER_APP_KEY"),  # optional
    base_url="https://api.cryptohopper.com/v1",       # default
    timeout=30.0,
    max_retries=3,
)
```

All keyword arguments except `api_key` are optional.

### `app_key`

Cryptohopper lets OAuth apps identify themselves on every request via the `x-api-app-key` header (value = your OAuth `client_id`). Set `app_key` on the client and the SDK adds that header automatically. This:

- Shows up in Cryptohopper's server-side telemetry, so you can attribute your own traffic.
- Drives per-app rate limits — if two apps share a token, they get independent quotas.
- Is harmless to omit. The server accepts unattributed requests.

### `base_url`

Override for staging or a local dev server. The default is `https://api.cryptohopper.com/v1`. The trailing `/v1` is part of the base; resource paths are relative to it.

```python
ch = CryptohopperClient(
    api_key=token,
    base_url="https://api.staging.cryptohopper.com/v1",
)
```

### `http_client`

If you need custom transport behaviour — proxies, custom CA bundles, connection pooling tuning — pass your own `httpx.Client`:

```python
import httpx

custom = httpx.Client(
    timeout=30.0,
    proxies="http://corporate-proxy.internal:3128",
    verify="/path/to/corporate-ca.pem",
)

with CryptohopperClient(api_key=token, http_client=custom) as ch:
    ...
# `custom` is NOT closed by `ch.close()` — you own its lifecycle.
```

When the SDK constructed the client itself, it owns it and closes it on `__exit__`. When you pass one in, it doesn't.

## IP allowlisting

If your Cryptohopper app has IP allowlisting enabled, requests from unlisted IPs return `403 FORBIDDEN`. The SDK surfaces this as `CryptohopperError` with `code == "FORBIDDEN"` and a populated `ip_address` field showing the IP Cryptohopper saw:

```python
from cryptohopper.errors import CryptohopperError

try:
    ch.hoppers.list()
except CryptohopperError as err:
    if err.code == "FORBIDDEN":
        print(f"Blocked from {err.ip_address}")
```

For CI where the runner IP isn't stable, either disable IP allowlisting for that app, or route outbound traffic through a stable IP (VPN, NAT gateway, dedicated proxy).

## Rotating tokens

Cryptohopper bearer tokens are long-lived but can be revoked:

- Manually from the dashboard.
- When the user revokes consent.

The SDK surfaces revocation as `UNAUTHORIZED` on the next call. There is no automatic refresh-token handling in the SDK today — if your app uses refresh tokens, handle the `UNAUTHORIZED` branch by exchanging your refresh token for a new access token, then retrying:

```python
def with_auto_refresh(call):
    try:
        return call()
    except CryptohopperError as err:
        if err.code != "UNAUTHORIZED":
            raise
        new_token = exchange_refresh_token()  # your code
        # `api_key` isn't mutable on the client — construct a new one.
        new_ch = CryptohopperClient(api_key=new_token)
        return call(new_ch)  # retry against the fresh client
```

The client's `api_key` is intentionally immutable. If you need to swap tokens often, construct fresh clients — the cost is small and it sidesteps subtle races where one in-flight request uses an old token while another uses the new one.

## Threading and concurrency

`CryptohopperClient` is built on `httpx.Client`, which is **safe to share across threads**. You don't need a client-per-thread; one client serving a thread pool is fine.

It is **not** an async client. For asyncio, wrap calls in `asyncio.to_thread`:

```python
import asyncio

async def fetch_hoppers(ch):
    return await asyncio.to_thread(ch.hoppers.list)
```

A first-class async client is a roadmap item; if you need it sooner, file an issue.

## Public-only access (no token)

A handful of endpoints accept anonymous calls:

- `/market/*` — marketplace browse
- `/platform/*` — i18n, country list, blog feed
- `/exchange/ticker`, `/exchange/candle`, `/exchange/orderbook`, `/exchange/markets`, `/exchange/exchanges`, `/exchange/forex-rates` — public market data

The SDK still requires `api_key` at construction; pass any non-empty placeholder if you only intend to hit public endpoints. The server ignores the bearer header on whitelisted routes.

```python
ch = CryptohopperClient(api_key="anonymous")  # placeholder; ignored on public routes
btc = ch.exchange.ticker(exchange="binance", market="BTC/USDT")
```
