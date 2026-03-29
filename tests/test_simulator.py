# tests/test_simulator.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Player, Team
from ds_engine import simulate_matchup


def make_team(name: str, pts: float, ast: float, dfn: float) -> Team:
    t = Team(name)
    for i in range(15):
        t.roster.append(Player(f"{name}_{i}", f"Player {i}", pts, ast, dfn))
    return t


def test_returns_winner_and_scores():
    a = make_team("Alpha", 25.0, 6.0, 5.0)
    b = make_team("Beta",  20.0, 4.0, 4.0)
    winner, score_a, score_b = simulate_matchup(a, b)
    assert winner in (a, b)
    assert isinstance(score_a, (int, float))
    assert isinstance(score_b, (int, float))
    assert score_a != score_b  # ties shouldn't happen with gauss


def test_stronger_team_wins_more_often():
    """Over 100 simulations, the stronger team should win ~55%+ of the time."""
    strong = make_team("Strong", 30.0, 8.0, 7.0)
    weak   = make_team("Weak",   10.0, 2.0, 2.0)
    strong_wins = 0
    for _ in range(100):
        winner, _, _ = simulate_matchup(strong, weak)
        if winner == strong:
            strong_wins += 1
    assert strong_wins >= 55, f"Expected strong team to win more often, got {strong_wins}/100"


def test_scores_are_positive():
    a = make_team("A", 20.0, 5.0, 5.0)
    b = make_team("B", 20.0, 5.0, 5.0)
    _, score_a, score_b = simulate_matchup(a, b)
    assert score_a > 0
    assert score_b > 0
