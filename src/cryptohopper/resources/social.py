"""``client.social`` — profiles, feed, posts, conversations, social graph."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import CryptohopperClient

AliasOrId = str | int
PostId = int | str


class Social:
    def __init__(self, client: CryptohopperClient) -> None:
        self._client = client

    # ─── Profiles ────────────────────────────────────────────────────────

    def get_profile(self, alias_or_id: AliasOrId) -> dict[str, Any]:
        """Fetch a public profile by alias or id. Requires ``read``."""
        return self._client._request(
            "GET", "/social/getprofile", params={"alias": alias_or_id}
        )

    def edit_profile(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update the authenticated user's own profile. Requires ``user``."""
        return self._client._request("POST", "/social/editprofile", json=data)

    def check_alias(self, alias: str) -> dict[str, Any]:
        """Check whether an alias is available."""
        return self._client._request(
            "GET", "/social/checkalias", params={"alias": alias}
        )

    # ─── Feed / discovery ────────────────────────────────────────────────

    def get_feed(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Personalised feed. Requires ``read``."""
        return self._client._request("GET", "/social/getfeed", params=params or None)

    def get_trends(self) -> Sequence[dict[str, Any]]:
        """Trending topics. Requires ``read``."""
        return self._client._request("GET", "/social/gettrends")

    def who_to_follow(self) -> Sequence[dict[str, Any]]:
        """Suggested profiles to follow. Requires ``read``."""
        return self._client._request("GET", "/social/whotofollow")

    def search(self, query: str) -> Sequence[dict[str, Any]]:
        """Search for posts / users. Requires ``read``."""
        return self._client._request("GET", "/social/search", params={"q": query})

    # ─── Notifications ───────────────────────────────────────────────────

    def get_notifications(self, **params: Any) -> Sequence[dict[str, Any]]:
        """Notifications for the authenticated user. Requires ``notifications``."""
        return self._client._request(
            "GET", "/social/getnotifications", params=params or None
        )

    # ─── Conversations / messages ────────────────────────────────────────

    def get_conversation_list(self) -> Sequence[dict[str, Any]]:
        """List the user's DM conversations. Requires ``read``."""
        return self._client._request("GET", "/social/getconversationlist")

    def get_conversation(
        self, conversation_id: int | str
    ) -> Sequence[dict[str, Any]]:
        """Load messages for a single conversation. Requires ``read``."""
        return self._client._request(
            "GET",
            "/social/loadconversation",
            params={"conversation_id": conversation_id},
        )

    def send_message(self, data: dict[str, Any]) -> dict[str, Any]:
        """Send a DM. Requires ``user``."""
        return self._client._request("POST", "/social/sendmessage", json=data)

    def delete_message(self, message_id: int | str) -> dict[str, Any]:
        """Delete a DM. Requires ``user``."""
        return self._client._request(
            "POST", "/social/deletemessage", json={"message_id": message_id}
        )

    # ─── Posts ───────────────────────────────────────────────────────────

    def create_post(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new post. Requires ``user``."""
        return self._client._request("POST", "/social/post", json=data)

    def get_post(self, post_id: PostId) -> dict[str, Any]:
        """Fetch a single post. Requires ``read``."""
        return self._client._request(
            "GET", "/social/getpost", params={"post_id": post_id}
        )

    def delete_post(self, post_id: PostId) -> dict[str, Any]:
        """Delete a post. Requires ``user``."""
        return self._client._request(
            "POST", "/social/deletepost", json={"post_id": post_id}
        )

    def pin_post(self, post_id: PostId) -> dict[str, Any]:
        """Pin/unpin a post on the user's profile. Requires ``user``."""
        return self._client._request(
            "POST", "/social/pinpost", json={"post_id": post_id}
        )

    # ─── Comments ────────────────────────────────────────────────────────

    def get_comment(self, comment_id: int | str) -> dict[str, Any]:
        """Fetch a single comment. Requires ``read``."""
        return self._client._request(
            "GET", "/social/getcomment", params={"comment_id": comment_id}
        )

    def get_comments(self, post_id: PostId) -> Sequence[dict[str, Any]]:
        """List comments on a post. Requires ``read``."""
        return self._client._request(
            "GET", "/social/getcomments", params={"post_id": post_id}
        )

    def delete_comment(self, comment_id: int | str) -> dict[str, Any]:
        """Delete a comment. Requires ``user``."""
        return self._client._request(
            "POST", "/social/deletecomment", json={"comment_id": comment_id}
        )

    # ─── Media ───────────────────────────────────────────────────────────

    def get_media(self, media_id: int | str) -> dict[str, Any]:
        """Fetch a media attachment. Requires ``read``."""
        return self._client._request(
            "GET", "/social/getmedia", params={"media_id": media_id}
        )

    # ─── Social graph ────────────────────────────────────────────────────

    def follow(self, alias_or_id: AliasOrId) -> dict[str, Any]:
        """Follow/unfollow. Requires ``user``."""
        return self._client._request(
            "POST", "/social/follow", json={"alias": alias_or_id}
        )

    def get_followers(self, alias_or_id: AliasOrId) -> Sequence[dict[str, Any]]:
        """List followers. Requires ``read``."""
        return self._client._request(
            "GET", "/social/followers", params={"alias": alias_or_id}
        )

    def get_following(self, alias_or_id: AliasOrId) -> dict[str, Any]:
        """Check whether the auth'd user follows the given profile. Requires ``read``."""
        return self._client._request(
            "GET", "/social/following", params={"alias": alias_or_id}
        )

    def get_following_profiles(
        self, alias_or_id: AliasOrId
    ) -> Sequence[dict[str, Any]]:
        """List profiles the given user follows. Requires ``read``."""
        return self._client._request(
            "GET",
            "/social/followingprofiles",
            params={"alias": alias_or_id},
        )

    # ─── Engagement ──────────────────────────────────────────────────────

    def like(self, post_id: PostId) -> dict[str, Any]:
        """Like/unlike a post. Requires ``user``."""
        return self._client._request("POST", "/social/like", json={"post_id": post_id})

    def repost(self, post_id: PostId) -> dict[str, Any]:
        """Repost a post. Requires ``user``."""
        return self._client._request(
            "POST", "/social/repost", json={"post_id": post_id}
        )

    # ─── Moderation ──────────────────────────────────────────────────────

    def block_user(self, alias_or_id: AliasOrId) -> dict[str, Any]:
        """Block a user. Requires ``user``."""
        return self._client._request(
            "POST", "/social/blockuser", json={"alias": alias_or_id}
        )
