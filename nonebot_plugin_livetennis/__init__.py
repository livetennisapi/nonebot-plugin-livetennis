"""nonebot-plugin-livetennis — live tennis scores, today's fixtures and
player lookup from the Live Tennis API (free tier), on demand only."""

from datetime import datetime, timezone

from nonebot import get_plugin_config, on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .client import LiveTennisClient, LiveTennisError
from .config import Config
from .render import (
    USAGE,
    format_live_matches,
    format_player_results,
    format_today,
)

__plugin_meta__ = PluginMetadata(
    name="Live Tennis 网球比分",
    description=(
        "Live tennis scores, today's fixtures and player rankings "
        "(ATP/WTA/Challenger/ITF/juniors) via the Live Tennis API "
        "/ 实时网球比分、今日赛程与球员排名查询"
    ),
    usage=USAGE,
    type="application",
    homepage="https://github.com/livetennisapi/nonebot-plugin-livetennis",
    config=Config,
    supported_adapters=None,
    extra={
        "author": "Synapse Research Ltd <hello@livetennisapi.com>",
        "version": "0.1.0",
    },
)

plugin_config = get_plugin_config(Config)

tennis = on_command("tennis", aliases={"网球"}, priority=10, block=True)

_MISSING_KEY = (
    "No API key configured. Set LIVETENNIS_API_KEY in your bot's .env — "
    "a free key (30 req/min, 100 req/day): "
    "https://livetennisapi.com/subscribe/free\n"
    "尚未配置 API 密钥。请在 .env 中设置 LIVETENNIS_API_KEY，"
    "免费密钥（每分钟 30 次、每天 100 次）申请地址："
    "https://livetennisapi.com/subscribe/free"
)

_LIVE_WORDS = {"live", "实时", "直播"}
_TODAY_WORDS = {"today", "今日", "今天"}
_PLAYER_WORDS = {"player", "球员", "选手"}


def _client() -> LiveTennisClient:
    return LiveTennisClient(
        api_key=plugin_config.livetennis_api_key,
        base_url=plugin_config.livetennis_api_base,
        timeout=plugin_config.livetennis_timeout,
    )


@tennis.handle()
async def handle_tennis(args: Message = CommandArg()) -> None:
    argv = args.extract_plain_text().strip().split()
    if not argv or argv[0].lower() in {"help", "帮助"}:
        await tennis.finish(USAGE)
    sub = argv[0].lower()
    if sub not in _LIVE_WORDS | _TODAY_WORDS | _PLAYER_WORDS:
        await tennis.finish(USAGE)
    if not plugin_config.livetennis_api_key:
        await tennis.finish(_MISSING_KEY)
    client = _client()
    try:
        if sub in _LIVE_WORDS:
            matches = await client.live_matches()
            await tennis.finish(
                format_live_matches(
                    matches, max_lines=plugin_config.livetennis_max_lines
                )
            )
        elif sub in _TODAY_WORDS:
            fixtures = await client.fixtures()
            today = datetime.now(timezone.utc).date()
            await tennis.finish(
                format_today(
                    fixtures, today, max_lines=plugin_config.livetennis_max_lines
                )
            )
        else:
            name = " ".join(argv[1:]).strip()
            if not name:
                await tennis.finish(
                    "Usage: /tennis player <name> / 用法：/网球 球员 <姓名>"
                )
            players = await client.search_players(name)
            await tennis.finish(format_player_results(players, name))
    except LiveTennisError as exc:
        await tennis.finish(str(exc))
