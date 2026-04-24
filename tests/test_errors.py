from cryptohopper.errors import CryptohopperError


def test_captures_code_status_message_server_code_and_ip() -> None:
    err = CryptohopperError(
        code="FORBIDDEN",
        message="This action requires 'trade' permission scope.",
        status=403,
        server_code=42,
        ip_address="203.0.113.42",
    )
    assert isinstance(err, Exception)
    assert err.code == "FORBIDDEN"
    assert err.status == 403
    assert err.server_code == 42
    assert err.ip_address == "203.0.113.42"
    assert str(err) == "This action requires 'trade' permission scope."


def test_unknown_string_codes_pass_through() -> None:
    err = CryptohopperError(code="SOMETHING_NEW", message="weird", status=418)
    assert err.code == "SOMETHING_NEW"


def test_retry_after_ms_optional() -> None:
    err = CryptohopperError(
        code="RATE_LIMITED", message="slow down", status=429, retry_after_ms=4000
    )
    assert err.retry_after_ms == 4000
