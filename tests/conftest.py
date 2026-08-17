import nonebot
import pytest
from nonebug import NONEBOT_INIT_KWARGS

BASE_URL = "https://api.livetennisapi.com/api/public/v1"

_INIT_KWARGS = {
    "driver": "~none",
    "livetennis_api_key": "test-key",
}

# Initialize at import time so test modules can import the plugin package
# at module level. nonebot.init is idempotent; nonebug's own session
# fixture becomes a no-op and only installs its matcher provider (which
# wraps, and therefore preserves, the already-registered matchers).
nonebot.init(**_INIT_KWARGS)

from nonebot.adapters.onebot.v11 import Adapter  # noqa: E402

nonebot.get_driver().register_adapter(Adapter)
nonebot.load_plugin("nonebot_plugin_livetennis")


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = _INIT_KWARGS
