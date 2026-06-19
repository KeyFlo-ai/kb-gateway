"""Bearer token verification for HTTP MCP (static API token)."""

from __future__ import annotations

from mcp.server.auth.provider import AccessToken

from .config import api_token


class StaticTokenVerifier:
    """Verify KB_GATEWAY_API_TOKEN bearer tokens."""

    def __init__(self, expected: str | None = None) -> None:
        self._expected = expected if expected is not None else api_token()

    async def verify_token(self, token: str) -> AccessToken | None:
        if not self._expected or token != self._expected:
            return None
        return AccessToken(
            token=token,
            client_id="kb-gateway",
            scopes=["learning:read"],
            subject="kb-gateway-client",
        )
