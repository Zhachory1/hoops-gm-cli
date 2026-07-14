import random

import ds_engine
from ds_engine import simulate_matchup
from models import Player, Team


def make_team(name: str, players: list[Player] | None = None) -> Team:
    team = Team(name)
    team.roster.extend(players or [])
    return team


def player(name: str, pts: float, ast: float, defense: float) -> Player:
    return Player(name.lower().replace(" ", "_"), name, pts, ast, defense)


def test_non_empty_rosters_return_integer_scores_and_winner(monkeypatch):
    monkeypatch.setattr(ds_engine.random, "gauss", lambda mu, sigma: mu)
    alpha = make_team("Alpha", [player("Alpha One", 20.0, 4.0, 2.0)])
    beta = make_team("Beta", [player("Beta One", 10.0, 1.0, 1.0)])

    winner, score_alpha, score_beta = simulate_matchup(alpha, beta)

    assert winner == alpha
    assert score_alpha == 20
    assert score_beta == 10
    assert isinstance(score_alpha, int)
    assert isinstance(score_beta, int)


def test_empty_rosters_tie_with_zero_scores():
    alpha = make_team("Alpha")
    beta = make_team("Beta")

    winner, score_alpha, score_beta = simulate_matchup(alpha, beta)

    assert winner == alpha
    assert score_alpha == 0
    assert score_beta == 0


def test_winner_selection_uses_higher_score(monkeypatch):
    monkeypatch.setattr(ds_engine.random, "gauss", lambda mu, sigma: mu)
    alpha = make_team("Alpha", [player("Alpha One", 5.0, 0.0, 0.0)])
    beta = make_team("Beta", [player("Beta One", 15.0, 0.0, 0.0)])

    winner, score_alpha, score_beta = simulate_matchup(alpha, beta)

    assert winner == beta
    assert score_beta > score_alpha


def test_negative_adjusted_scores_are_floored_at_zero(monkeypatch):
    monkeypatch.setattr(ds_engine.random, "gauss", lambda mu, sigma: -4.2)
    alpha = make_team("Alpha", [player("Alpha One", 1.0, 0.0, 0.0)])
    beta = make_team("Beta", [player("Beta One", 1.0, 0.0, 0.0)])

    _, score_alpha, score_beta = simulate_matchup(alpha, beta)

    assert score_alpha == 0
    assert score_beta == 0


def test_seeded_random_is_deterministic():
    alpha = make_team("Alpha", [player("Alpha One", 20.0, 4.0, 2.0)])
    beta = make_team("Beta", [player("Beta One", 10.0, 1.0, 1.0)])

    random.seed(42)
    first = simulate_matchup(alpha, beta)
    random.seed(42)
    second = simulate_matchup(alpha, beta)

    assert (first[0].name, first[1], first[2]) == (second[0].name, second[1], second[2])
