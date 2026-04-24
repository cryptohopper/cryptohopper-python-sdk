"""``client.webhooks`` — developer webhook registration.

Maps to the server's ``/api/webhook_*`` endpoints; namespace name chosen
for clarity over path mirroring.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

WebhookId = int | str


class Webhooks:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Register a new webhook (URL + event types)."""
        return self._client._request("POST", "/api/webhook_create", json=data)

    def delete(self, webhook_id: WebhookId) -> dict[str, Any]:
        """Delete a registered webhook."""
        return self._client._request(
            "POST", "/api/webhook_delete", json={"webhook_id": webhook_id}
        )
