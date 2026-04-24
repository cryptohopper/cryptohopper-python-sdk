"""One sanity test per new A1 resource — method, path, body shape."""

from __future__ import annotations

import json

from pytest_httpx import HTTPXMock

from cryptohopper import CryptohopperClient


def test_signals_list(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": []})
    client.signals.list()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/signals/signals"


def test_signals_chart_data_uses_single_word_path(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.signals.chart_data()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/signals/chartdata"


def test_arbitrage_exchange_vs_market_start(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.arbitrage.exchange_start({"hopper_id": 1})
    req1 = httpx_mock.get_request()
    assert req1 is not None
    assert str(req1.url) == "https://api.cryptohopper.com/v1/arbitrage/exchange"

    httpx_mock.add_response(json={"data": {}})
    client.arbitrage.market_start({"hopper_id": 2})
    req2 = httpx_mock.get_requests()[1]
    assert str(req2.url) == "https://api.cryptohopper.com/v1/arbitrage/market"


def test_arbitrage_market_cancel_uses_hyphenated_path(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.arbitrage.market_cancel()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/arbitrage/market-cancel"


def test_arbitrage_delete_backlog(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.arbitrage.delete_backlog(7)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert json.loads(req.read()) == {"backlog_id": 7}


def test_marketmaker_get(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.marketmaker.get(hopper_id=1)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["hopper_id"] == "1"


def test_marketmaker_set_market_trend(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.marketmaker.set_market_trend({"hopper_id": 1, "trend": "bull"})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/marketmaker/set-market-trend"
    assert json.loads(req.read()) == {"hopper_id": 1, "trend": "bull"}


def test_marketmaker_backlog_by_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 9}})
    client.marketmaker.backlog(9)
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == (
        "https://api.cryptohopper.com/v1/marketmaker/get-backlog?backlog_id=9"
    )


def test_template_list(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": []})
    client.template.list()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/template/templates"


def test_template_save_uses_hyphenated_path(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 4}})
    client.template.save({"name": "my template", "hopper_id": 1})
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/template/save-template"


def test_template_load_sends_both_ids(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.template.load(3, 5)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert json.loads(req.read()) == {"template_id": 3, "hopper_id": 5}
