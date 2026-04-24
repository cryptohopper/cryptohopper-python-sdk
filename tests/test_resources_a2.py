"""One sanity test per A2 resource — method, path, body shape."""

from __future__ import annotations

import json

from pytest_httpx import HTTPXMock

from cryptohopper import CryptohopperClient


def test_ai_available_models(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.ai.available_models()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/ai/availablemodels"


def test_ai_get_credits_preserves_server_prefix(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"balance": 100}})
    out = client.ai.get_credits()
    assert out["balance"] == 100
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/ai/getaicredits"


def test_ai_llm_analyze(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {"job_id": 7}})
    client.ai.llm_analyze({"strategy_id": 42})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/ai/doaillmanalyze"
    assert json.loads(req.read()) == {"strategy_id": 42}


def test_platform_search_documentation(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.platform.search_documentation("rsi")
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["q"] == "rsi"


def test_platform_bot_types(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.platform.bot_types()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/platform/bottypes"


def test_chart_share_save_hyphenated_path(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.chart.share_save({"title": "BTC chart"})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/chart/share-save"


def test_chart_delete_sends_chart_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.chart.delete(5)
    req = httpx_mock.get_request()
    assert req is not None
    assert json.loads(req.read()) == {"chart_id": 5}


def test_subscription_plans(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.subscription.plans()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/subscription/plans"


def test_subscription_hopper_sends_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.subscription.hopper(42)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["hopper_id"] == "42"


def test_subscription_stop(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.subscription.stop_subscription()
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == (
        "https://api.cryptohopper.com/v1/subscription/stopsubscription"
    )
