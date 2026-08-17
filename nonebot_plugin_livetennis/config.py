"""Plugin configuration, read from the NoneBot env (`.env` / environment)."""

from pydantic import BaseModel


class Config(BaseModel):
    """Configuration for nonebot-plugin-livetennis.

    Set these in your bot's ``.env`` file, e.g.::

        LIVETENNIS_API_KEY=ltapi_xxxxxxxx
    """

    livetennis_api_key: str = ""
    """Live Tennis API key. A free key: https://livetennisapi.com/subscribe/free"""

    livetennis_api_base: str = "https://api.livetennisapi.com/api/public/v1"
    """API base URL. You normally never change this."""

    livetennis_timeout: float = 10.0
    """HTTP timeout in seconds for API calls."""

    livetennis_max_lines: int = 12
    """Maximum number of matches/fixtures rendered per reply."""
