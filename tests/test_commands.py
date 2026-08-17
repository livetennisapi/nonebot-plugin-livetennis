import httpx
import nonebot
import respx
from nonebug import App

from .conftest import BASE_URL
from .samples import FIXTURE_TODAY, LIVE_MATCH, PLAYER


def fake_event(text: str):
    from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
    from nonebot.adapters.onebot.v11.event import Sender

    return PrivateMessageEvent(
        time=1_700_000_000,
        self_id=123456,
        post_type="message",
        sub_type="friend",
        user_id=654321,
        message_type="private",
        message_id=1,
        message=Message(text),
        original_message=Message(text),
        raw_message=text,
        font=0,
        sender=Sender(user_id=654321),
    )


async def run_command(app: App, text: str, expected: str) -> None:
    from nonebot.adapters.onebot.v11 import Adapter, Bot

    from nonebot_plugin_livetennis import tennis

    async with app.test_matcher(tennis) as ctx:
        adapter = nonebot.get_adapter(Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_event(text)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, expected, result=None)
        ctx.should_finished(tennis)


async def test_usage_on_bare_command(app: App):
    from nonebot_plugin_livetennis.render import USAGE

    await run_command(app, "/tennis", USAGE)


async def test_usage_on_unknown_subcommand(app: App):
    from nonebot_plugin_livetennis.render import USAGE

    await run_command(app, "/tennis frobnicate", USAGE)


@respx.mock
async def test_live_command(app: App):
    from nonebot_plugin_livetennis.render import format_live_matches

    respx.get(f"{BASE_URL}/matches").mock(
        return_value=httpx.Response(200, json={"data": [LIVE_MATCH], "meta": {}})
    )
    await run_command(app, "/tennis live", format_live_matches([LIVE_MATCH]))


@respx.mock
async def test_live_command_chinese_alias(app: App):
    from nonebot_plugin_livetennis.render import format_live_matches

    respx.get(f"{BASE_URL}/matches").mock(
        return_value=httpx.Response(200, json={"data": [LIVE_MATCH], "meta": {}})
    )
    await run_command(app, "/网球 实时", format_live_matches([LIVE_MATCH]))


@respx.mock
async def test_today_command(app: App):
    from datetime import datetime, timezone

    from nonebot_plugin_livetennis.render import format_today

    respx.get(f"{BASE_URL}/fixtures").mock(
        return_value=httpx.Response(200, json={"data": [FIXTURE_TODAY], "meta": {}})
    )
    today = datetime.now(timezone.utc).date()
    await run_command(app, "/tennis today", format_today([FIXTURE_TODAY], today))


@respx.mock
async def test_player_command(app: App):
    from nonebot_plugin_livetennis.render import format_player_results

    respx.get(f"{BASE_URL}/players").mock(
        return_value=httpx.Response(200, json={"data": [PLAYER], "meta": {}})
    )
    await run_command(
        app, "/tennis player alcaraz", format_player_results([PLAYER], "alcaraz")
    )


async def test_player_without_name(app: App):
    await run_command(
        app, "/tennis player", "Usage: /tennis player <name> / 用法：/网球 球员 <姓名>"
    )


@respx.mock
async def test_api_error_reported_to_user(app: App):
    respx.get(f"{BASE_URL}/matches").mock(return_value=httpx.Response(429))
    from nonebot_plugin_livetennis.client import _ERROR_MESSAGES

    await run_command(app, "/tennis live", _ERROR_MESSAGES[429])


async def test_missing_key_message(app: App, monkeypatch):
    import nonebot_plugin_livetennis as plugin

    monkeypatch.setattr(plugin.plugin_config, "livetennis_api_key", "")
    await run_command(app, "/tennis live", plugin._MISSING_KEY)
