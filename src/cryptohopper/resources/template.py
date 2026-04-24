"""``client.template`` — bot templates (reusable hopper configurations)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

TemplateId = int | str


class Templates:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    def list(self) -> Sequence[dict[str, Any]]:
        """List all templates the user has access to. Requires ``read``."""
        return self._client._request("GET", "/template/templates")

    def get(self, template_id: TemplateId) -> dict[str, Any]:
        """Fetch a template. Requires ``read``."""
        return self._client._request(
            "GET", "/template/get", params={"template_id": template_id}
        )

    def basic(self, template_id: TemplateId) -> dict[str, Any]:
        """Fetch the basic (lightweight) view of a template. Requires ``read``."""
        return self._client._request(
            "GET", "/template/basic", params={"template_id": template_id}
        )

    def save(self, data: dict[str, Any]) -> dict[str, Any]:
        """Save a new template. Requires ``manage``."""
        return self._client._request("POST", "/template/save-template", json=data)

    def update(
        self, template_id: TemplateId, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing template. Requires ``manage``."""
        return self._client._request(
            "POST", "/template/update", json={"template_id": template_id, **data}
        )

    def load(
        self, template_id: TemplateId, hopper_id: TemplateId
    ) -> dict[str, Any]:
        """Apply a template to a hopper. Requires ``manage``."""
        return self._client._request(
            "POST",
            "/template/load",
            json={"template_id": template_id, "hopper_id": hopper_id},
        )

    def delete(self, template_id: TemplateId) -> dict[str, Any]:
        """Delete a template. Requires ``manage``."""
        return self._client._request(
            "POST", "/template/delete", json={"template_id": template_id}
        )
