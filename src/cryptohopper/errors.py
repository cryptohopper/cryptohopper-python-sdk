"""Single exception type raised by every SDK call on non-2xx responses
(and on network/timeout failures).

Unknown backend codes pass through in ``.code`` as raw strings so callers
can add handling without waiting for an SDK update.
"""

from __future__ import annotations

from typing import Literal

KnownCryptohopperErrorCode = Literal[
    "VALIDATION_ERROR",
    "UNAUTHORIZED",
    "FORBIDDEN",
    "NOT_FOUND",
    "CONFLICT",
    "RATE_LIMITED",
    "SERVER_ERROR",
    "SERVICE_UNAVAILABLE",
    "DEVICE_UNAUTHORIZED",
    "NETWORK_ERROR",
    "TIMEOUT",
    "UNKNOWN",
]

CryptohopperErrorCode = str


class CryptohopperError(Exception):
    """Raised by every SDK call on failure.

    Attributes:
        code: Short machine-readable error code derived from HTTP status
            (see ``KnownCryptohopperErrorCode``).
        status: HTTP status code; 0 for network / timeout failures.
        server_code: Numeric ``code`` field from the Cryptohopper error
            envelope, when present (e.g. the rate-limit bucket identifier).
        ip_address: Client IP the server saw. Useful for debugging IP
            whitelist mismatches on OAuth apps.
        retry_after_ms: Populated on 429 from the ``Retry-After`` header.
    """

    code: CryptohopperErrorCode
    status: int
    server_code: int | None
    ip_address: str | None
    retry_after_ms: int | None

    def __init__(
        self,
        *,
        code: CryptohopperErrorCode,
        message: str,
        status: int,
        server_code: int | None = None,
        ip_address: str | None = None,
        retry_after_ms: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.server_code = server_code
        self.ip_address = ip_address
        self.retry_after_ms = retry_after_ms

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return (
            f"CryptohopperError(code={self.code!r}, status={self.status}, "
            f"ip_address={self.ip_address!r}, message={str(self)!r})"
        )
