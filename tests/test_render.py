from datetime import date

from nonebot_plugin_livetennis.render import (
    format_fixture,
    format_live_match,
    format_live_matches,
    format_player,
    format_player_results,
    format_score,
    format_today,
    is_break_point,
)

from .samples import FIXTURE_TODAY, FIXTURE_TOMORROW, LIVE_MATCH, PLAYER

TODAY = date(2026, 8, 17)


class TestBreakPoint:
    def test_receiver_at_40_server_below(self):
        score = {"server": 1, "points": ["30", "40"], "is_tiebreak": False}
        assert is_break_point(score) is True

    def test_receiver_at_ad(self):
        score = {"server": 2, "points": ["AD", "40"], "is_tiebreak": False}
        assert is_break_point(score) is True

    def test_deuce_is_not_break_point(self):
        score = {"server": 1, "points": ["40", "40"], "is_tiebreak": False}
        assert is_break_point(score) is False

    def test_server_ahead(self):
        score = {"server": 1, "points": ["40", "30"], "is_tiebreak": False}
        assert is_break_point(score) is False

    def test_never_in_tiebreak(self):
        score = {"server": 1, "points": ["3", "6"], "is_tiebreak": True}
        assert is_break_point(score) is False

    def test_null_points_absent(self):
        score = {"server": 1, "points": [None, None], "is_tiebreak": False}
        assert is_break_point(score) is False

    def test_null_server_absent(self):
        score = {"server": None, "points": ["0", "40"], "is_tiebreak": False}
        assert is_break_point(score) is False

    def test_no_score(self):
        assert is_break_point(None) is False


class TestFormatScore:
    def test_full_score(self):
        assert format_score(LIVE_MATCH["score"]) == "6-4 3-3 (30-40)"

    def test_tiebreak_prefix(self):
        score = {
            "sets": [0, 0],
            "games": [[6], [6]],
            "points": ["5", "3"],
            "is_tiebreak": True,
        }
        assert format_score(score) == "6-6 (TB 5-3)"

    def test_null_points_omitted(self):
        score = {"sets": [1, 0], "games": [[6], [4]], "points": [None, None]}
        assert format_score(score) == "6-4"

    def test_empty(self):
        assert format_score(None) == ""


class TestLiveRendering:
    def test_single_match(self):
        text = format_live_match(LIVE_MATCH)
        assert text == (
            "[ATP] Cincinnati Masters QF\n"
            "  Carlos Alcaraz* vs Jannik Sinner — 6-4 3-3 (30-40) [BP 破发点]"
        )

    def test_list_header_and_body(self):
        text = format_live_matches([LIVE_MATCH])
        assert text.startswith("Live now / 实时比分 (1):")
        assert "Carlos Alcaraz*" in text

    def test_empty_list(self):
        text = format_live_matches([])
        assert "No live matches" in text
        assert "没有正在进行" in text

    def test_truncation(self):
        text = format_live_matches([LIVE_MATCH] * 15, max_lines=12)
        assert "+3 more" in text


class TestToday:
    def test_filters_to_today(self):
        text = format_today([FIXTURE_TODAY, FIXTURE_TOMORROW], TODAY)
        assert "Iga Swiatek vs Aryna Sabalenka" in text
        assert "Casper Ruud" not in text

    def test_fixture_line(self):
        line = format_fixture(FIXTURE_TODAY)
        assert line == (
            "15:00 UTC  Iga Swiatek vs Aryna Sabalenka (Cincinnati Masters SF)"
        )

    def test_no_fixtures_today(self):
        text = format_today([FIXTURE_TOMORROW], TODAY)
        assert "No fixtures scheduled" in text
        assert "今日" in text

    def test_null_start_time_is_tba(self):
        line = format_fixture(FIXTURE_TOMORROW)
        assert line.startswith("TBA")


class TestPlayer:
    def test_full_profile(self):
        text = format_player(PLAYER)
        assert text == (
            "Carlos Alcaraz [ES]\n"
            "Tour / 巡回赛: atp\n"
            "Ranking / 排名: #2 (8600 pts) ↑\n"
            "Hand / 持拍手: right / 右手\n"
            "Backhand / 反手: two-handed / 双反\n"
            "Born / 出生: 2003-05-05"
        )

    def test_unranked(self):
        text = format_player({"name": "Nobody Q", "ranking": None})
        assert "unranked / 无排名" in text

    def test_no_results(self):
        text = format_player_results([], "zzz")
        assert "No player found" in text
        assert "未找到球员" in text

    def test_also_matched(self):
        second = {"id": 3, "name": "Someone Else"}
        text = format_player_results([PLAYER, second], "alc")
        assert "Also matched / 其他匹配: Someone Else" in text
