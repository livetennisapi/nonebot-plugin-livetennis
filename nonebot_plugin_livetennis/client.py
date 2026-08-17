"""Thin async client for the Live Tennis API (free-tier endpoints only).

Endpoints used — all FREE tier per the published OpenAPI spec
(https://github.com/livetennisapi/openapi):

- ``GET /matches?status=live``  — live matches with latest score
- ``GET /fixtures``             — upcoming scheduled fixtures, earliest first
- ``GET /players?search=``      — player search (a player's own current
  ranking is on the player object at FREE tier)
"""

from typing import Any, Optional

import httpx


class LiveTennisError(Exception):
    """Raised for any API failure; ``str(err)`` is a bilingual, user-safe message."""


_ERROR_MESSAGES = {
    401: (
        "Invalid or missing API key. Get a free key at "
        "https://livetennisapi.com/subscribe/free and set LIVETENNIS_API_KEY.\n"
        "API 密钥无效或缺失。请在 https://livetennisapi.com/subscribe/free "
        "免费申请密钥并配置 LIVETENNIS_API_KEY。"
    ),
    403: ("This request needs a higher plan tier. / 该请求需要更高的订阅等级。"),
    429: (
        "Rate limit reached (free tier: 30 req/min, 100 req/day). "
        "Please try again in a minute.\n"
        "已达到调用频率限制（免费版：每分钟 30 次，每天 100 次），请稍后再试。"
    ),
}


class LiveTennisClient:
    """One short-lived HTTP request per call; no connection is held open."""

    def __init__(self, api_key: str, base_url: str, timeout: float = 10.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as http:
                resp = await http.get(
                    f"{self._base_url}{path}",
                    params=params,
                    headers={"X-API-Key": self._api_key},
                )
        except httpx.HTTPError as exc:
            raise LiveTennisError(
                "Could not reach the Live Tennis API (network error). "
                "/ 无法连接 Live Tennis API（网络错误）。"
            ) from exc
        if resp.status_code != 200:
            message = _ERROR_MESSAGES.get(
                resp.status_code,
                f"Live Tennis API error / 接口错误 (HTTP {resp.status_code})",
            )
            raise LiveTennisError(message)
        try:
            return resp.json()
        except ValueError as exc:
            raise LiveTennisError(
                "Unexpected response from the Live Tennis API. / 接口返回异常。"
            ) from exc

    async def live_matches(self, limit: int = 50) -> list[dict[str, Any]]:
        payload = await self._get("/matches", {"status": "live", "limit": limit})
        return payload.get("data") or []

    async def fixtures(self, limit: int = 50) -> list[dict[str, Any]]:
        payload = await self._get("/fixtures", {"limit": limit})
        return payload.get("data") or []

    async def search_players(self, name: str, limit: int = 5) -> list[dict[str, Any]]:
        payload = await self._get("/players", {"search": name, "limit": limit})
        return payload.get("data") or []
