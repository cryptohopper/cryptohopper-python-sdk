# Changelog

All notable changes to the `cryptohopper` Python package are documented in this file.
The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.3.0a1 — Unreleased

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
