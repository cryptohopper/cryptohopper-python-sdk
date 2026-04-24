"""One sanity test per A3 resource — method, path, body shape."""

from __future__ import annotations

import json

from pytest_httpx import HTTPXMock

from cryptohopper import CryptohopperClient


def test_social_get_profile(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"alias": "pim"}})
    client.social.get_profile("pim")
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/social/getprofile?alias=pim"


def test_social_create_post_maps_to_bare_post(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 1}})
    client.social.create_post({"content": "hi"})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/social/post"


def test_social_get_conversation_maps_to_loadconversation(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.social.get_conversation(42)
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == (
        "https://api.cryptohopper.com/v1/social/loadconversation"
        "?conversation_id=42"
    )


def test_social_like_posts_post_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.social.like(99)
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert json.loads(req.read()) == {"post_id": 99}


def test_tournaments_list_hits_gettournaments(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.tournaments.list()
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/tournaments/gettournaments"


def test_tournaments_tournament_leaderboard(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": []})
    client.tournaments.tournament_leaderboard(7)
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == (
        "https://api.cryptohopper.com/v1/tournaments/leaderboard_tournament"
        "?tournament_id=7"
    )


def test_tournaments_join_merges_id(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.tournaments.join(5, {"team": "alpha"})
    req = httpx_mock.get_request()
    assert req is not None
    assert json.loads(req.read()) == {"tournament_id": 5, "team": "alpha"}


def test_webhooks_create(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {"id": 1}})
    client.webhooks.create({"url": "https://example.com/hook"})
    req = httpx_mock.get_request()
    assert req is not None
    assert req.method == "POST"
    assert str(req.url) == "https://api.cryptohopper.com/v1/api/webhook_create"


def test_webhooks_delete(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.webhooks.delete(42)
    req = httpx_mock.get_request()
    assert req is not None
    assert json.loads(req.read()) == {"webhook_id": 42}


def test_app_in_app_purchase_underscored_path(
    httpx_mock: HTTPXMock, client: CryptohopperClient
) -> None:
    httpx_mock.add_response(json={"data": {}})
    client.app.in_app_purchase({"receipt": "abc"})
    req = httpx_mock.get_request()
    assert req is not None
    assert str(req.url) == "https://api.cryptohopper.com/v1/app/in_app_purchase"
