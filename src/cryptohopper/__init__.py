"""Official Python SDK for the Cryptohopper API.

Quickstart::

    from cryptohopper import CryptohopperClient

    with CryptohopperClient(api_key="ch_...") as ch:
        me = ch.user.get()
        ticker = ch.exchange.ticker(exchange="binance", market="BTC/USDT")
"""

from ._client import CryptohopperClient
from ._version import CURRENT_VERSION
from .errors import CryptohopperError, CryptohopperErrorCode, KnownCryptohopperErrorCode

__all__ = [
    "CURRENT_VERSION",
    "CryptohopperClient",
    "CryptohopperError",
    "CryptohopperErrorCode",
    "KnownCryptohopperErrorCode",
]
