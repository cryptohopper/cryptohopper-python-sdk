"""Transport layer tests with ``pytest-httpx``."""

from __future__ import annotations

import httpx
import pytest
from pytest_httpx import HTTPXMock

from cryptohopper import CURRENT_VERSION, CryptohopperClient, CryptohopperError


def test_bearer_user_agent_and_data_unwrap(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(
        url="https://api.cryptohopper.com/v1/user/get",
        json={"data": {"hello": "world"}},
    )
    out = client._request("GET", "/user/get")
    assert out == {"hello": "world"}

    req = httpx_mock.get_request()
    assert req is not None
    assert req.headers["Authorization"] == "Bearer ch_test"
    assert req.headers["User-Agent"] == f"cryptohopper-sdk-python/{CURRENT_VERSION}"
    assert "x-api-app-key" not in req.headers


def test_app_key_sets_header(httpx_mock: HTTPXMock) -> None:
    client = CryptohopperClient(api_key="ch_test", app_key="client_123", max_retries=0)
    httpx_mock.add_response(json={"data": {}})
    client._request("GET", "/user/get")
    req = httpx_mock.get_request()
    assert req is not None
    assert req.headers["x-api-app-key"] == "client_123"
    client.close()


def test_post_attaches_json_body(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {"ok": True}})
    client._request("POST", "/x", json={"foo": 1})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.read() == b'{"foo":1}'
    assert req.headers["Content-Type"].startswith("application/json")


def test_query_params_sent(httpx_mock: HTTPXMock, client: CryptohopperClient) -> None:
    httpx_mock.add_response(json={"data": {}})
    client._request(
        "GET",
        "/exchange/ticker",
        params={"exchange": "binance", "market": "BTC/USDT", "skip": None},
    )
    req = httpx_mock.get_request()
    assert req is not None
    assert req.url.params["exchange"] == "binance"
    assert req.url.params["market"] == "BTC/USDT"
    assert "skip" not in req.url.params  # None values stripped


def test_cryptohopper_error_envelope_maps_to_typed_exception(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(
        status_code=403,
        json={
            "status": 403,
            "code": 0,
            "error": 1,
            "message": "This action requires 'trade' permission scope.",
            "ip_address": "203.0.113.42",
        },
    )
    with pytest.raises(CryptohopperError) as exc:
        client._request("GET", "/x")
    assert exc.value.code == "FORBIDDEN"
    assert exc.value.status == 403
    assert exc.value.ip_address == "203.0.113.42"
    assert str(exc.value) == "This action requires 'trade' permission scope."


def test_retry_on_429_honours_retry_after_and_succeeds(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        status_code=429,
        headers={"retry-after": "0"},
        json={"status": 429, "code": 0, "error": 1, "message": "Rate limit reached"},
    )
    httpx_mock.add_response(json={"data": {"ok": True}})
    c = CryptohopperClient(api_key="ch_test", max_retries=2, timeout=5.0)
    out = c._request("GET", "/x")
    assert out == {"ok": True}
    assert len(httpx_mock.get_requests()) == 2
    c.close()


def test_gives_up_after_max_retries_on_persistent_429(httpx_mock: HTTPXMock) -> None:
    for _ in range(3):
        httpx_mock.add_response(
            status_code=429,
            headers={"retry-after": "0"},
            json={"status": 429, "code": 0, "error": 1, "message": "slow"},
        )
    c = CryptohopperClient(api_key="ch_test", max_retries=2, timeout=5.0)
    with pytest.raises(CryptohopperError) as exc:
        c._request("GET", "/x")
    assert exc.value.code == "RATE_LIMITED"
    assert len(httpx_mock.get_requests()) == 3
    c.close()


def test_network_error_maps_to_network_error(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_exception(httpx.ConnectError("ECONNREFUSED"))
    with pytest.raises(CryptohopperError) as exc:
        client._request("GET", "/x")
    assert exc.value.code == "NETWORK_ERROR"
    assert exc.value.status == 0


def test_non_json_5xx_falls_back_to_server_error(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(status_code=500, text="upstream crashed")
    with pytest.raises(CryptohopperError) as exc:
        client._request("GET", "/x")
    assert exc.value.code == "SERVER_ERROR"
    assert exc.value.status == 500


def test_custom_base_url() -> None:
    c = CryptohopperClient(
        api_key="ch_test",
        base_url="https://api-staging.cryptohopper.com/v1/",
    )
    assert c.base_url == "https://api-staging.cryptohopper.com/v1"
    c.close()


def test_empty_api_key_rejected() -> None:
    with pytest.raises(TypeError, match="api_key"):
        CryptohopperClient(api_key="")
