# Changelog

All notable changes to the `cryptohopper` Python package are documented in this file.
The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.4.0a2 — Unreleased

### Fixed
- **Critical: every authenticated request was rejected by the API gateway.** The transport sent `Authorization: Bearer <token>`, which the AWS API Gateway in front of `api.cryptohopper.com/v1/*` rejects (it routes `Authorization` to a SigV4 parser and returns `405 Missing Authentication Token`). Cryptohopper's Public API v1 uses `access-token: <token>` instead — confirmed by the official [API documentation](https://www.cryptohopper.com/api-documentation/how-the-api-works) and the legacy `cryptohopper-ios-sdk` / `cryptohopper-android-sdk`. Switching the SDK to send `access-token`. The `Authorization` header is no longer set.
- The `app_key` → `x-api-app-key` header is unchanged; that one was always correct.

### Compatibility
No public-API change. The fix is purely in the request-builder and is invisible to callers — `client.user.get()`, `client.hoppers.list()`, etc. all keep their existing signatures and behaviour. Only the wire-level header sent on each request changes.

## 0.4.0a1 — 2026-04-25

Adds four more API domains: `social`, `tournaments`, `webhooks`, `app`. Final A-wave — all 14 remaining public domains now covered.

### Added
- **`social`** (27 methods) — profiles, feed, trends, search, notifications, conversations/messages, posts, comments, media, follows, likes/reposts, moderation.
- **`tournaments`** (11 methods) — `list`, `active`, `get`, `search`, `trades`, `stats`, `activity`, `leaderboard`, `tournament_leaderboard`, `join`, `leave`.
- **`webhooks`** (2 methods) — developer webhook registration (maps to `/api/webhook_*`).
- **`app`** (2 methods) — mobile app store `receipt` + `in_app_purchase`.

## 0.3.0a1 — 2026-04-24

Adds four more API domains: `ai`, `platform`, `chart`, `subscription`.

### Added
- **`ai`** — `list`, `get`, `available_models`, `get_credits`, `credit_invoices`, `credit_transactions`, `buy_credits`, `llm_analyze_options`, `llm_analyze`, `llm_analyze_results`, `llm_results`.
- **`platform`** — `latest_blog`, `documentation`, `promo_bar`, `search_documentation`, `countries`, `country_allowlist`, `ip_country`, `languages`, `bot_types` (all public).
- **`chart`** — `list`, `get`, `save`, `delete`, `share_save`, `share_get`.
- **`subscription`** — `hopper`, `get`, `plans`, `remap`, `assign`, `get_credits`, `order_sub`, `stop_subscription`.

## 0.2.0a1 — 2026-04-24

Adds four more API domains: `signals`, `arbitrage`, `marketmaker`, `template`.

### Added
- **`signals`** — `list`, `performance`, `stats`, `distribution`, `chart_data`.
- **`arbitrage`** — `exchange_start`, `exchange_cancel`, `exchange_results`, `exchange_history`, `exchange_total`, `exchange_reset_total`, `market_start`, `market_cancel`, `market_result`, `market_history`, `backlogs`, `backlog`, `delete_backlog`.
- **`marketmaker`** — `get`, `cancel`, `history`, `get_market_trend`, `set_market_trend`, `delete_market_trend`, `backlogs`, `backlog`, `delete_backlog`.
- **`template`** — `list`, `get`, `basic`, `save`, `update`, `load`, `delete`.

## 0.1.0a1 — 2026-04-24

Initial release. Covers six core API domains.

### Transport
- `CryptohopperClient` — OAuth2 bearer auth, optional `app_key` sent as `x-api-app-key`, context-manager support.
- `CryptohopperError` — typed exception with `code`, `status`, `server_code`, `ip_address`, `retry_after_ms`.
- Automatic retry on HTTP 429 honouring `Retry-After` (default `max_retries=3`, configurable/disableable).
- Configurable `timeout`, injectable `httpx.Client`, optional `user_agent` suffix.

### Resources
- `user` — `get`
- `hoppers` — `list`, `get`, `create`, `update`, `delete`, `positions`, `position`, `orders`, `buy`, `sell`, `config_get`, `config_update`, `config_pools`, `panic`
- `exchange` — `ticker`, `candles`, `orderbook`, `markets`, `currencies`, `exchanges`, `forex_rates`
- `strategy` — `list`, `get`, `create`, `update`, `delete`
- `backtest` — `create`, `get`, `list`, `cancel`, `restart`, `limits`
- `market` — `signals`, `signal`, `items`, `item`, `homepage`
