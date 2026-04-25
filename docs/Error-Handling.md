# Error Handling

Every non-2xx response and every transport failure raises `CryptohopperError`. Same shape across every official Cryptohopper SDK in every language.

```python
from cryptohopper.errors import CryptohopperError

try:
    ch.hoppers.get(999_999)
except CryptohopperError as err:
    print({
        "code": err.code,                  # "NOT_FOUND"
        "status": err.status,              # 404
        "message": str(err),               # human-readable
        "server_code": err.server_code,    # numeric Cryptohopper code (or None)
        "ip_address": err.ip_address,      # server-reported caller IP (or None)
        "retry_after_ms": err.retry_after_ms,  # only set on 429
    })
```

## Error code catalog

| `code` | HTTP | When you'll see it | Recover by |
|---|---|---|---|
| `VALIDATION_ERROR` | 400, 422 | Missing or malformed parameter | Fix the request; the message says which parameter |
| `UNAUTHORIZED` | 401 | Token missing, wrong, or revoked | Re-auth; your refresh flow kicks in |
| `DEVICE_UNAUTHORIZED` | 402 | Internal Cryptohopper device-auth flow rejected you | You shouldn't see this via the public API; contact support if you do |
| `FORBIDDEN` | 403 | Scope missing, or IP not allowlisted | Check `err.ip_address`; add to allowlist or grant the scope on the app |
| `NOT_FOUND` | 404 | Resource or endpoint doesn't exist | Check the ID; check you're using the latest SDK |
| `CONFLICT` | 409 | Resource is in a conflicting state | Cancel the existing job or wait |
| `RATE_LIMITED` | 429 | Bucket exhausted | The SDK auto-retries; see [Rate Limits](Rate-Limits.md) |
| `SERVER_ERROR` | 500–502, 504 | Cryptohopper's end | Retry with back-off; report if persistent |
| `SERVICE_UNAVAILABLE` | 503 | Planned maintenance or downstream outage | Respect `Retry-After`; retry |
| `NETWORK_ERROR` | — | DNS failure, TCP reset, TLS handshake failure | Retry; check your network |
| `TIMEOUT` | — | Hit the client-side `timeout` | Retry; bump `timeout` if the operation is legitimately slow |
| `UNKNOWN` | any | Anything else the SDK didn't recognise | Inspect `err.status` and `str(err)` |

These strings are stable across SDK versions — compare with `==`, never substring-match.

## Catching specific codes

`CryptohopperError` is a single exception type with a discriminating `code` attribute. There are no per-code subclasses (deliberate — keeps the API small and matches every other Cryptohopper SDK):

```python
try:
    ch.hoppers.create(data)
except CryptohopperError as err:
    if err.code == "VALIDATION_ERROR":
        # Missing field. Show the user.
        log.warning("Bad payload: %s", err)
    elif err.code in {"UNAUTHORIZED", "FORBIDDEN"}:
        # Token problem. Re-auth.
        refresh_and_retry()
    elif err.code == "RATE_LIMITED":
        # SDK already retried `max_retries` times. Back off harder.
        sleep_long_and_retry()
    else:
        # Not an SDK-known case — log and re-raise.
        log.exception("Unexpected Cryptohopper error")
        raise
```

The literal type `KnownCryptohopperErrorCode` is exported if you want a `match` statement with an exhaustiveness check:

```python
from cryptohopper.errors import CryptohopperError, KnownCryptohopperErrorCode
from typing import assert_never

def handle(err: CryptohopperError) -> str:
    code = err.code  # narrowed by mypy if you cast it
    match code:
        case "UNAUTHORIZED" | "FORBIDDEN":
            return "auth"
        case "RATE_LIMITED":
            return "throttled"
        case "VALIDATION_ERROR":
            return "bad-request"
        case "NETWORK_ERROR" | "TIMEOUT":
            return "transient"
        case _:
            return "other"
```

Note: at runtime `err.code` is `str`, not the `Literal` union — the server can return codes the SDK doesn't recognise (unprefixed pass-through). Don't write code that crashes if a new code appears.

## The retry surface

- **429 retries are automatic** up to `max_retries` (default 3). The SDK parses `Retry-After` and honours it. See [Rate Limits](Rate-Limits.md) for the algorithm.
- **Everything else you handle yourself.** `SERVER_ERROR` and `NETWORK_ERROR` are often transient and benefit from retry; `UNAUTHORIZED` / `VALIDATION_ERROR` / `NOT_FOUND` never do.

## A robust retry wrapper

```python
import time
from collections.abc import Callable
from typing import TypeVar
from cryptohopper.errors import CryptohopperError

T = TypeVar("T")
TRANSIENT = {"SERVER_ERROR", "SERVICE_UNAVAILABLE", "NETWORK_ERROR", "TIMEOUT"}

def with_retry(fn: Callable[[], T], *, max_attempts: int = 5, base_ms: int = 500) -> T:
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except CryptohopperError as err:
            if err.code not in TRANSIENT or attempt == max_attempts:
                raise
            wait_ms = err.retry_after_ms or base_ms * (2 ** (attempt - 1))
            time.sleep(wait_ms / 1000.0)
    raise RuntimeError("unreachable")
```

Don't include `RATE_LIMITED` in `TRANSIENT` — the SDK already retries 429s internally. Wrapping `RATE_LIMITED` in another retry layer would multiply attempts unhelpfully.

## JSON-friendly error serialization

When you're piping SDK errors through a structured logger:

```python
def err_to_dict(err: BaseException) -> dict[str, object]:
    if isinstance(err, CryptohopperError):
        return {
            "kind": "cryptohopper",
            "code": err.code,
            "status": err.status,
            "message": str(err),
            "server_code": err.server_code,
            "ip_address": err.ip_address,
            "retry_after_ms": err.retry_after_ms,
        }
    return {
        "kind": type(err).__name__,
        "message": str(err),
    }
```

Plays well with structlog, loguru, and the stdlib `logging` JSON formatters.
