# Getting Started

## Install

```bash
pip install cryptohopper
```

Requires Python 3.10 or newer. Works with `pip`, `uv`, `poetry`, `pipenv`, and any other resolver that reads `pyproject.toml`.

## First call

```python
import os
from cryptohopper import CryptohopperClient

with CryptohopperClient(api_key=os.environ["CRYPTOHOPPER_TOKEN"]) as ch:
    me = ch.user.get()
    print("Logged in as:", me["email"])
```

The client is a context manager — using `with` ensures the underlying `httpx.Client` is closed even on exceptions. If you can't use a context manager (e.g. a long-running daemon), construct it once and call `ch.close()` on shutdown:

```python
ch = CryptohopperClient(api_key=os.environ["CRYPTOHOPPER_TOKEN"])
try:
    while True:
        do_work(ch)
finally:
    ch.close()
```

## Getting a token

Every request (except a handful of public endpoints like `/exchange/ticker`) needs an OAuth2 bearer token. Create one via **Developer → Create App** on [cryptohopper.com](https://www.cryptohopper.com) and complete the consent flow. The token is a 40-character opaque string.

For local dev, the simplest path is:

```bash
export CRYPTOHOPPER_TOKEN=<your-token>
```

In production, store the token in your secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, etc.) and load it at startup.

## Common pitfalls

**`ImportError: cannot import name 'CryptohopperClient'`** — the package is `cryptohopper`, not `cryptohopper-sdk`. Verify with `pip show cryptohopper`.

**`TypeError: CryptohopperClient: 'api_key' is required`** — you passed an empty string or `None`. Check that your env var is actually set in the process running the code:

```python
import os
print("token:", os.environ.get("CRYPTOHOPPER_TOKEN", "MISSING"))
```

**`UNAUTHORIZED` on every call** — the token is wrong, expired, or revoked. Visit the app's page in the Cryptohopper dashboard and check the status.

**`FORBIDDEN` on endpoints that used to work** — IP allowlisting on the OAuth app blocked your current IP. The error includes `ip_address` so you can see what Cryptohopper saw:

```python
from cryptohopper import CryptohopperClient
from cryptohopper.errors import CryptohopperError

try:
    ch.hoppers.list()
except CryptohopperError as err:
    if err.code == "FORBIDDEN":
        print(f"Blocked from {err.ip_address}")
```

**`SSL: CERTIFICATE_VERIFY_FAILED`** — corporate proxy or self-signed root CA in your chain. Don't disable verification globally; use httpx's `verify` argument with a path to the proper CA bundle:

```python
import httpx
custom_client = httpx.Client(verify="/path/to/corporate/ca-bundle.pem", timeout=30.0)
ch = CryptohopperClient(
    api_key=os.environ["CRYPTOHOPPER_TOKEN"],
    http_client=custom_client,
)
```

When you bring your own `httpx.Client`, the SDK won't close it for you — manage its lifetime yourself.

## Type hints

Every public method has full type hints. If you use mypy or pyright, the SDK plays well with strict mode:

```python
from cryptohopper import CryptohopperClient
from cryptohopper.errors import CryptohopperError

reveal_type(CryptohopperClient)  # CryptohopperClient
reveal_type(ch.hoppers.list())   # list[dict[str, Any]]
```

Response shapes are typed as `dict[str, Any]` because Cryptohopper's API hasn't been frozen into stable models yet. If you want to layer pydantic / dataclass parsing on top, you can — the SDK won't fight you.

## Next steps

- [Authentication](Authentication.md) — deeper dive on tokens, app keys, IP whitelisting
- [Error Handling](Error-Handling.md) — every error code and how to recover
- [Rate Limits](Rate-Limits.md) — auto-retry, customizing back-off, high-volume patterns
