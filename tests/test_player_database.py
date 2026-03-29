# tests/test_player_database.py
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Player
from ds_engine import PlayerDatabase

PLAYERS = [
    Player("p1631238", "Michael Devoe",   4.67, 1.0,  0.0),
    Player("p78357",   "Irv Torgoff",     2.0,  0.0,  0.0),
    Player("p1631128", "Christian Braun", 8.76, 1.67, 1.02),
]


def test_get_by_id_returns_correct_player():
    db = PlayerDatabase()
    for p in PLAYERS:
        db.load(p)
    result = db.get_player_by_id("p78357")
    assert result is not None
    assert result.name == "Irv Torgoff"


def test_get_by_name_returns_correct_player():
    db = PlayerDatabase()
    for p in PLAYERS:
        db.load(p)
    result = db.get_player_by_name("Michael Devoe")
    assert result is not None
    assert result.id == "p1631238"


def test_missing_id_returns_none():
    db = PlayerDatabase()
    assert db.get_player_by_id("p999") is None


def test_missing_name_returns_none():
    db = PlayerDatabase()
    assert db.get_player_by_name("Nobody Real") is None


def test_load_all_players_all_retrievable():
    db = PlayerDatabase()
    raw = json.load(open("data/players.json"))
    players = [Player(**p) for p in raw]
    for p in players:
        db.load(p)
    for p in players:
        assert db.get_player_by_id(p.id) is not None
        assert db.get_player_by_name(p.name) is not None
