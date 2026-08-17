"""Shared sample payloads shaped like the published OpenAPI schemas."""

LIVE_MATCH = {
    "id": 101,
    "tournament": "Cincinnati Masters",
    "tour": "atp",
    "tournament_id": "atp-cincinnati",
    "round": "Quarterfinal",
    "round_code": "QF",
    "status": "live",
    "is_doubles": False,
    "players": {
        "p1": {"id": 1, "name": "Carlos Alcaraz", "country": "ES", "ranking": 2},
        "p2": {"id": 2, "name": "Jannik Sinner", "country": "IT", "ranking": 1},
    },
    "score": {
        "sets": [1, 0],
        "games": [[6, 3], [4, 3]],
        "points": ["30", "40"],
        "server": 1,
        "is_tiebreak": False,
    },
}

FIXTURE_TODAY = {
    "id": 7,
    "event_date": "2026-08-17",
    "start_time": "2026-08-17T15:00:00Z",
    "player1_name": "Iga Swiatek",
    "player2_name": "Aryna Sabalenka",
    "tournament": "Cincinnati Masters",
    "round_code": "SF",
    "tour": "wta",
    "status": "upcoming",
}

FIXTURE_TOMORROW = {
    "id": 8,
    "event_date": "2026-08-18",
    "start_time": None,
    "player1_name": "Casper Ruud",
    "player2_name": "Alexander Zverev",
    "tournament": "Cincinnati Masters",
    "round_code": "SF",
    "tour": "atp",
    "status": "upcoming",
}

PLAYER = {
    "id": 1,
    "name": "Carlos Alcaraz",
    "country": "ES",
    "tour": "atp",
    "ranking": 2,
    "ranking_points": 8600,
    "ranking_movement": "up",
    "hand": "R",
    "backhand": 2,
    "birthday": "2003-05-05",
    "is_doubles_team": False,
}
