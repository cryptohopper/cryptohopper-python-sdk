"""Shared fixtures: build a CryptohopperClient wired to ``pytest-httpx``."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from cryptohopper import CryptohopperClient


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> CryptohopperClient:  # noqa: ARG001 - fixture wiring
    """A CryptohopperClient pointed at the default base URL; all HTTP is mocked."""
    return CryptohopperClient(
        api_key="ch_test",
        timeout=5.0,
        max_retries=0,  # transport tests should not retry unless they opt in
    )
