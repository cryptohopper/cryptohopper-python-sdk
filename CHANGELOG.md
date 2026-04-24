# Changelog

All notable changes to the `cryptohopper` Python package are documented in this file.
The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.1.0a1 — Unreleased

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
