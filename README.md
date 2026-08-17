# nonebot-plugin-livetennis

Live tennis scores, today's fixtures and player rankings in your NoneBot2 bot — ATP, WTA, Challenger, ITF and juniors, powered by the [Live Tennis API](https://livetennisapi.com).

> **Disclosure / 声明:** This plugin is written and maintained by the Live Tennis API team — it is vendor-authored. / 本插件由 Live Tennis API 官方团队编写和维护。

[English](#english) | [简体中文](#简体中文)

---

## English

### What it does

On-demand chat commands (no background polling, no schedulers):

| Command | Alias | What you get |
|---|---|---|
| `/tennis live` | `/网球 实时` | Matches in play right now, with set/game/point score, who is serving (`*`) and a break-point marker |
| `/tennis today` | `/网球 今日` | Today's scheduled fixtures (UTC), earliest first |
| `/tennis player <name>` | `/网球 球员 <姓名>` | Player search: country, tour, current world ranking, plays/backhand, birth date |
| `/tennis` | `/网球` | Bilingual help |

Works on any adapter that can send plain text (`supported_adapters=None`).

### Tier truth

Everything this plugin calls is on the **free** tier of the Live Tennis API: live scores (score/server/break-point state), players (including a player's own current ranking), fixtures and usage. The free tier allows **30 requests/minute and 100 requests/day** — plenty for on-demand chat commands, but honestly **not** enough for continuous fast polling, which is why this plugin only calls the API when someone asks. (The rank-ordered rankings *listing* is a Pro endpoint; this plugin does not use it — it shows the ranking carried on the free player object.)

### Install

Once the package is published on PyPI (pending):

```bash
pip install nonebot-plugin-livetennis
# or
nb plugin install nonebot-plugin-livetennis
```

Working today, straight from git:

```bash
pip install git+https://github.com/livetennisapi/nonebot-plugin-livetennis.git
```

Then enable it in your bot's `pyproject.toml`:

```toml
[tool.nonebot]
plugins = ["nonebot_plugin_livetennis"]
```

### Configure

Get a free API key at <https://livetennisapi.com/subscribe/free> and add it to your bot's `.env`:

```dotenv
LIVETENNIS_API_KEY=your-key-here
```

Optional settings (defaults shown):

```dotenv
LIVETENNIS_API_BASE=https://api.livetennisapi.com/api/public/v1
LIVETENNIS_TIMEOUT=10.0
LIVETENNIS_MAX_LINES=12
```

### Example output

```
Live now / 实时比分 (1):
[ATP] Cincinnati Masters QF
  Carlos Alcaraz* vs Jannik Sinner — 6-4 3-3 (30-40) [BP 破发点]
```

`*` marks the server; `[BP]` appears when the receiver holds a break point (receiver at AD, or at 40 with the server on 0/15/30 — never shown in tiebreaks or when the state is unknown).

### Development

```bash
pip install -e . --group dev
ruff check . && ruff format --check .
pytest
```

Docs: <https://docs.livetennisapi.com> · Spec: [livetennisapi/openapi](https://github.com/livetennisapi/openapi)

---

## 简体中文

### 功能

按需触发的聊天指令（无后台轮询、无定时任务）：

| 指令 | 别名 | 内容 |
|---|---|---|
| `/tennis live` | `/网球 实时` | 当前进行中的比赛：盘/局/分比分、发球方（`*`）与破发点标记 |
| `/tennis today` | `/网球 今日` | 今日赛程（UTC），按时间先后排列 |
| `/tennis player <name>` | `/网球 球员 <姓名>` | 球员搜索：国籍、巡回赛、当前世界排名、持拍手/反手、出生日期 |
| `/tennis` | `/网球` | 双语帮助 |

支持所有能发送纯文本的适配器（`supported_adapters=None`）。

### 套餐说明（如实）

本插件调用的全部接口均属于 Live Tennis API 的**免费**套餐：实时比分（比分/发球方/破发点状态）、球员（含球员自身的当前排名）、赛程与用量查询。免费套餐限额为**每分钟 30 次、每天 100 次**——足够按需查询使用，但**不**适合持续高频轮询，因此本插件只在用户发出指令时才调用接口。（按名次排序的排名*列表*属于 Pro 接口，本插件不使用它，而是展示免费球员对象上自带的排名。）

### 安装

PyPI 发布后（待发布）：

```bash
pip install nonebot-plugin-livetennis
# 或
nb plugin install nonebot-plugin-livetennis
```

当前可直接从 git 安装：

```bash
pip install git+https://github.com/livetennisapi/nonebot-plugin-livetennis.git
```

然后在机器人的 `pyproject.toml` 中启用：

```toml
[tool.nonebot]
plugins = ["nonebot_plugin_livetennis"]
```

### 配置

在 <https://livetennisapi.com/subscribe/free> 免费申请 API 密钥，写入机器人的 `.env`：

```dotenv
LIVETENNIS_API_KEY=你的密钥
```

可选配置（默认值如下）：

```dotenv
LIVETENNIS_API_BASE=https://api.livetennisapi.com/api/public/v1
LIVETENNIS_TIMEOUT=10.0
LIVETENNIS_MAX_LINES=12
```

### 输出示例

```
Live now / 实时比分 (1):
[ATP] Cincinnati Masters QF
  Carlos Alcaraz* vs Jannik Sinner — 6-4 3-3 (30-40) [BP 破发点]
```

`*` 表示发球方；当接发球方握有破发点时显示 `[BP 破发点]`（接发球方 AD，或接发球方 40 而发球方为 0/15/30；抢七局不显示，状态未知时不显示）。

文档：<https://docs.livetennisapi.com> · 接口规范：[livetennisapi/openapi](https://github.com/livetennisapi/openapi)

## License

MIT © Live Tennis API
