"""One sanity test per resource — method, path, and body shape."""

from __future__ import annotations

import json

from pytest_httpx import HTTPXMock

from cryptohopper import CryptohopperClient


def test_hoppers_list_sends_exchange_filter(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.hoppers.list(exchange="binance")
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "GET"
    assert str(req.url).startswith("https://api.cryptohopper.com/v1/hopper/list")
    assert req.url.params["exchange"] == "binance"


def test_hoppers_get_sends_hopper_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 42}})
    client.hoppers.get(42)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["hopper_id"] == "42"


def test_hoppers_buy_posts_json(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.hoppers.buy({"hopper_id": 42, "market": "BTC/USDT", "amount": "0.001"})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/hopper/buy"
    assert json.loads(req.read()) == {
        "hopper_id": 42,
        "market": "BTC/USDT",
        "amount": "0.001",
    }


def test_hoppers_config_update_merges_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.hoppers.config_update(7, {"strategy_id": 99})
    req = httpx_mock.get_request()
    assert req is not None
    assert json.loads(req.read()) == {"hopper_id": 7, "strategy_id": 99}


def test_hoppers_panic(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.hoppers.panic(5)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/hopper/panic"


def test_exchange_ticker(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {"last": 42000}})
    out = client.exchange.ticker(exchange="binance", market="BTC/USDT")
    assert out["last"] == 42000
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["exchange"] == "binance"
    assert req.url.params["market"] == "BTC/USDT"


def test_exchange_candles_passes_timeframe(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.exchange.candles(exchange="binance", market="BTC/USDT", timeframe="1h")
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url).startswith("https://api.cryptohopper.com/v1/exchange/candle")
    assert req.url.params["timeframe"] == "1h"


def test_exchange_exchanges_no_params(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.exchange.exchanges()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/exchange/exchanges"


def test_strategy_list_hits_plural_endpoint(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.strategy.list()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/strategy/strategies"


def test_strategy_update_hits_edit(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.strategy.update(5, {"name": "renamed"})
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/strategy/edit"
    assert json.loads(req.read()) == {"strategy_id": 5, "name": "renamed"}


def test_backtest_create_hits_new(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 1}})
    client.backtest.create({"hopper_id": 42})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/backtest/new"


def test_backtest_limits(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {"remaining": 3, "limit": 5}})
    out = client.backtest.limits()
    assert out["remaining"] == 3


def test_market_items_uses_marketitems_endpoint(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.market.items(type="strategy")
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url).startswith(
        "https://api.cryptohopper.com/v1/market/marketitems"
    )
    assert req.url.params["type"] == "strategy"


def test_market_signal_by_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 99}})
    client.market.signal(99)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["signal_id"] == "99"


def test_user_get_hits_user_get(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 1, "email": "x@y.com"}})
    out = client.user.get()
    assert out["email"] == "x@y.com"
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/user/get"
