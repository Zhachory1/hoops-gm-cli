# tests/test_sort.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Player
from ds_engine import merge_sort


def make_players():
    return [
        Player("p1", "Alpha",   20.0, 5.0, 6.0),
        Player("p2", "Beta",    30.0, 2.0, 4.0),
        Player("p3", "Gamma",   10.0, 9.0, 8.0),
        Player("p4", "Delta",   25.0, 7.0, 3.0),
        Player("p5", "Epsilon", 15.0, 3.0, 9.0),
    ]


def test_sort_by_points_descending():
    players = make_players()
    result = merge_sort(players, "points_avg")
    pts = [p.points_avg for p in result]
    assert pts == sorted(pts, reverse=True)


def test_sort_by_assists_descending():
    players = make_players()
    result = merge_sort(players, "assists_avg")
    vals = [p.assists_avg for p in result]
    assert vals == sorted(vals, reverse=True)


def test_sort_by_defense_descending():
    players = make_players()
    result = merge_sort(players, "defense_rating")
    vals = [p.defense_rating for p in result]
    assert vals == sorted(vals, reverse=True)


def test_sort_does_not_mutate_input():
    players = make_players()
    original_order = [p.name for p in players]
    merge_sort(players, "points_avg")
    assert [p.name for p in players] == original_order


def test_sort_single_element():
    players = [Player("p1", "Solo", 20.0, 5.0, 6.0)]
    result = merge_sort(players, "points_avg")
    assert len(result) == 1


def test_sort_empty_list():
    assert merge_sort([], "points_avg") == []
