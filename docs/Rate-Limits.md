# Rate Limits

Cryptohopper applies per-bucket rate limits on the server. When you hit one, you get a `429` with a `Retry-After` header. The SDK handles this for you.

## The default behaviour

On every `429`, the SDK:

1. Parses `Retry-After` (either seconds or HTTP-date form).
2. Sleeps that long (falling back to exponential back-off if the header is missing).
3. Retries the request.
4. Repeats up to `max_retries` (default 3).

If retries exhaust, you get a `CryptohopperError` with `code == "RATE_LIMITED"` and `retry_after_ms` set to the last seen retry hint.

## Configuring it

```python
ch = CryptohopperClient(
    api_key=token,
    max_retries=10,    # default 3
    timeout=60.0,      # default 30s; bump if your retries push past 30s total
)
```

To **disable** retries entirely (e.g. you want to do your own back-off):

```python
ch = CryptohopperClient(api_key=token, max_retries=0)
```

With `max_retries=0` a 429 surfaces immediately as `RATE_LIMITED`. Your code can inspect `err.retry_after_ms` and schedule the retry on its own timeline.

## Per-call override

The transport accepts a `max_retries=` override on a per-call basis (internal API; see `_client.CryptohopperClient._request`). You usually don't need this — set it on the client and forget it.

## Buckets

Cryptohopper has three named buckets:

| Bucket | Scope | Example endpoints |
|---|---|---|
| `normal` | Most reads + writes | `/user/get`, `/hopper/list`, `/hopper/update`, `/exchange/ticker` |
| `order` | Anything that places or modifies orders | `/hopper/buy`, `/hopper/sell`, `/hopper/panic` |
| `backtest` | The (expensive) backtest subsystem | `/backtest/new`, `/backtest/get` |

The SDK doesn't know which bucket a call is against — it only sees the 429. You don't need to either; the server tells you when you're limited.

## Hitting limits intentionally (backfill jobs)

If you're ingesting historical data and need to fetch many pages, take ownership of the back-off logic:

```python
import time
from cryptohopper import CryptohopperClient
from cryptohopper.errors import CryptohopperError

with CryptohopperClient(api_key=token, max_retries=0) as ch:
    for hopper_id in all_hopper_ids:
        while True:
            try:
                orders = ch.hoppers.orders(hopper_id)
                process(orders)
                break
            except CryptohopperError as err:
                if err.code == "RATE_LIMITED":
                    wait = (err.retry_after_ms or 1000) / 1000.0
                    time.sleep(wait)
                    continue
                raise
```

This pattern lets a long-running job honour rate limits without stalling other work, because you decide the pacing.

## What the SDK does NOT do

- **No global semaphore.** If you spawn 50 threads each calling the SDK and the server rate-limits them, every thread's retry is independent — you might get 50 simultaneous sleeps. For high-concurrency workloads, cap concurrency yourself with a `concurrent.futures.ThreadPoolExecutor` or `multiprocessing.dummy.Pool`.
- **No adaptive slow-down.** After a 429, the SDK waits and retries that one call — it doesn't throttle future calls. If you see frequent 429s, lower your concurrency or add explicit sleeps between calls.
- **No client-side bucket tracking.** The server is the source of truth.

## Combining with concurrent.futures

A pragmatic pattern for parallelism with rate-limit awareness:

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_one(hopper_id: str) -> dict:
    return ch.hoppers.get(hopper_id)  # 429s auto-retried by the SDK

with ThreadPoolExecutor(max_workers=4) as pool:
    # Cap concurrency at 4 — much higher and you'll trip rate limits
    # despite the SDK's per-call retries.
    results = list(pool.map(fetch_one, all_hopper_ids))
```

Empirically, **4–8 concurrent workers** is comfortable for most accounts. Higher is feasible with `app_key` set (which gives your OAuth app its own quota) but plan to back off explicitly.

## Diagnosing "always rate-limited"

If every request returns `RATE_LIMITED` even at low volume:

1. Check that your app hasn't been flagged for abuse in the Cryptohopper dashboard.
2. Check that you haven't accidentally created a loop that retries on non-429 errors too.
3. Check `err.server_code` — Cryptohopper sometimes includes a numeric detail there that clarifies which bucket you've tripped.
4. Check that you're not sharing a token across many machines (one quota, divided across all of them).
