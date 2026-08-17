"""Pure formatting helpers — no I/O, fully unit-testable."""

from datetime import date, datetime
from typing import Any, Optional

Match = dict[str, Any]

USAGE = (
    "Live Tennis commands / 网球指令:\n"
    "/tennis live — live scores now / 当前实时比分\n"
    "/tennis today — today's schedule / 今日赛程\n"
    "/tennis player <name> — player search & ranking / 球员搜索与排名\n"
    "Aliases / 别名: /网球 实时 | 今日 | 球员 <姓名>\n"
    "Data / 数据: Live Tennis API (free tier) — https://livetennisapi.com"
)


def is_break_point(score: Optional[dict[str, Any]]) -> bool:
    """Break point: receiver at AD, or receiver at 40 while the server is at
    0/15/30. Never in a tiebreak; False when server or points are unknown."""
    if not score or score.get("is_tiebreak"):
        return False
    server = score.get("server")
    points = score.get("points") or []
    if server not in (1, 2) or len(points) < 2:
        return False
    server_pts = points[server - 1]
    receiver_pts = points[2 - server]
    if server_pts is None or receiver_pts is None:
        return False
    return receiver_pts == "AD" or (
        receiver_pts == "40" and server_pts in ("0", "15", "30")
    )


def format_score(score: Optional[dict[str, Any]]) -> str:
    """``6-4 3-2 (30-40)`` from a Score object; '' when there is no score."""
    if not score:
        return ""
    games = score.get("games") or []
    parts: list[str] = []
    if len(games) == 2 and games[0] is not None and games[1] is not None:
        parts.extend(f"{g1}-{g2}" for g1, g2 in zip(games[0], games[1]))
    points = score.get("points") or []
    if len(points) >= 2 and points[0] is not None and points[1] is not None:
        current = f"{points[0]}-{points[1]}"
        if score.get("is_tiebreak"):
            current = f"TB {current}"
        parts.append(f"({current})")
    return " ".join(parts)


def _match_header(match: Match) -> str:
    tour = match.get("tour")
    bits = [f"[{tour.upper()}]"] if tour else []
    tournament = match.get("tournament")
    if tournament:
        bits.append(str(tournament))
    round_code = match.get("round_code") or match.get("round")
    if round_code:
        bits.append(str(round_code))
    return " ".join(bits)


def format_live_match(match: Match) -> str:
    players = match.get("players") or {}
    p1 = (players.get("p1") or {}).get("name") or "?"
    p2 = (players.get("p2") or {}).get("name") or "?"
    score = match.get("score")
    server = (score or {}).get("server")
    if server == 1:
        p1 += "*"
    elif server == 2:
        p2 += "*"
    line = f"{p1} vs {p2}"
    rendered = format_score(score)
    if rendered:
        line += f" — {rendered}"
    if is_break_point(score):
        line += " [BP 破发点]"
    header = _match_header(match)
    return f"{header}\n  {line}" if header else f"  {line}"


def format_live_matches(matches: list[Match], max_lines: int = 12) -> str:
    if not matches:
        return "No live matches right now. / 当前没有正在进行的比赛。"
    shown = matches[:max_lines]
    body = "\n".join(format_live_match(m) for m in shown)
    head = f"Live now / 实时比分 ({len(matches)}):"
    tail = ""
    if len(matches) > len(shown):
        rest = len(matches) - len(shown)
        tail = f"\n… +{rest} more / 还有 {rest} 场"
    return f"{head}\n{body}{tail}"


def _fixture_is_today(fixture: Match, today: date) -> bool:
    event_date = fixture.get("event_date")
    if event_date:
        return event_date == today.isoformat()
    start_time = fixture.get("start_time")
    if start_time:
        try:
            return (
                datetime.fromisoformat(start_time.replace("Z", "+00:00")).date()
                == today
            )
        except ValueError:
            return False
    return False


def format_fixture(fixture: Match) -> str:
    p1 = fixture.get("player1_name") or "?"
    p2 = fixture.get("player2_name") or "?"
    start_time = fixture.get("start_time")
    when = "TBA"
    if start_time:
        try:
            parsed = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            when = parsed.strftime("%H:%M UTC")
        except ValueError:
            when = str(start_time)
    bits = [f"{when}  {p1} vs {p2}"]
    tournament = fixture.get("tournament")
    round_code = fixture.get("round_code") or fixture.get("round")
    context = " ".join(str(b) for b in (tournament, round_code) if b)
    if context:
        bits.append(f"({context})")
    return " ".join(bits)


def format_today(fixtures: list[Match], today: date, max_lines: int = 12) -> str:
    todays = [f for f in fixtures if _fixture_is_today(f, today)]
    if not todays:
        return (
            f"No fixtures scheduled for today ({today.isoformat()} UTC). "
            "/ 今日（UTC）暂无赛程。"
        )
    shown = todays[:max_lines]
    body = "\n".join(format_fixture(f) for f in shown)
    head = f"Today's schedule / 今日赛程 {today.isoformat()} (UTC):"
    tail = ""
    if len(todays) > len(shown):
        rest = len(todays) - len(shown)
        tail = f"\n… +{rest} more / 还有 {rest} 场"
    return f"{head}\n{body}{tail}"


_HAND = {"R": "right / 右手", "L": "left / 左手"}
_BACKHAND = {1: "one-handed / 单反", 2: "two-handed / 双反"}
_MOVEMENT = {"up": "↑", "down": "↓", "same": "="}


def format_player(player: Match) -> str:
    name = player.get("name") or "?"
    country = player.get("country")
    title = f"{name} [{country}]" if country else name
    lines = [title]
    tour = player.get("tour")
    if tour:
        lines.append(f"Tour / 巡回赛: {tour}")
    ranking = player.get("ranking")
    if ranking is not None:
        rank_line = f"Ranking / 排名: #{ranking}"
        points = player.get("ranking_points")
        if points is not None:
            rank_line += f" ({points} pts)"
        movement = _MOVEMENT.get(player.get("ranking_movement") or "")
        if movement:
            rank_line += f" {movement}"
        lines.append(rank_line)
    else:
        lines.append("Ranking / 排名: unranked / 无排名")
    hand = _HAND.get(player.get("hand") or "")
    if hand:
        lines.append(f"Hand / 持拍手: {hand}")
    backhand = _BACKHAND.get(player.get("backhand") or 0)
    if backhand:
        lines.append(f"Backhand / 反手: {backhand}")
    birthday = player.get("birthday")
    if birthday:
        lines.append(f"Born / 出生: {birthday}")
    return "\n".join(lines)


def format_player_results(players: list[Match], query: str) -> str:
    if not players:
        return (
            f"No player found for '{query}'. / 未找到球员“{query}”。\n"
            "Try the family name in Latin letters. / 请尝试使用拉丁字母姓氏搜索。"
        )
    text = format_player(players[0])
    others = [p.get("name") for p in players[1:] if p.get("name")]
    if others:
        text += "\nAlso matched / 其他匹配: " + ", ".join(str(o) for o in others)
    return text
