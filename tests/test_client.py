import httpx
import pytest
import respx

from nonebot_plugin_livetennis.client import LiveTennisClient, LiveTennisError

from .conftest import BASE_URL
from .samples import LIVE_MATCH, PLAYER


def make_client() -> LiveTennisClient:
    return LiveTennisClient(api_key="test-key", base_url=BASE_URL)


@respx.mock
async def test_live_matches_sends_key_and_params():
    route = respx.get(f"{BASE_URL}/matches").mock(
        return_value=httpx.Response(200, json={"data": [LIVE_MATCH], "meta": {}})
    )
    matches = await make_client().live_matches()
    assert matches == [LIVE_MATCH]
    request = route.calls.last.request
    assert request.headers["X-API-Key"] == "test-key"
    assert request.url.params["status"] == "live"


@respx.mock
async def test_search_players():
    respx.get(f"{BASE_URL}/players").mock(
        return_value=httpx.Response(200, json={"data": [PLAYER], "meta": {}})
    )
    players = await make_client().search_players("alcaraz")
    assert players[0]["name"] == "Carlos Alcaraz"


@respx.mock
async def test_fixtures_empty_data():
    respx.get(f"{BASE_URL}/fixtures").mock(
        return_value=httpx.Response(200, json={"data": [], "meta": {}})
    )
    assert await make_client().fixtures() == []


@respx.mock
async def test_401_maps_to_key_message():
    respx.get(f"{BASE_URL}/matches").mock(return_value=httpx.Response(401))
    with pytest.raises(LiveTennisError, match="Invalid or missing API key"):
        await make_client().live_matches()


@respx.mock
async def test_429_maps_to_rate_limit_message():
    respx.get(f"{BASE_URL}/matches").mock(return_value=httpx.Response(429))
    with pytest.raises(LiveTennisError, match="Rate limit"):
        await make_client().live_matches()


@respx.mock
async def test_network_error_is_wrapped():
    respx.get(f"{BASE_URL}/matches").mock(side_effect=httpx.ConnectError)
    with pytest.raises(LiveTennisError, match="network error"):
        await make_client().live_matches()


@respx.mock
async def test_unknown_status_carries_code():
    respx.get(f"{BASE_URL}/matches").mock(return_value=httpx.Response(500))
    with pytest.raises(LiveTennisError, match="HTTP 500"):
        await make_client().live_matches()
