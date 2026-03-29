# tests/test_bst.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Team
from ds_engine import BST


def make_teams():
    teams = [
        Team("Alpha"),
        Team("Beta"),
        Team("Gamma"),
        Team("Delta"),
    ]
    teams[0].wins, teams[0].losses = 10, 4
    teams[1].wins, teams[1].losses = 7,  7
    teams[2].wins, teams[2].losses = 12, 2
    teams[3].wins, teams[3].losses = 5,  9
    return teams


def test_inorder_returns_descending_wins():
    bst = BST()
    for t in make_teams():
        bst.insert(t)
    result = bst.inorder()
    wins = [t.wins for t in result]
    assert wins == sorted(wins, reverse=True)


def test_inorder_returns_all_teams():
    bst = BST()
    for t in make_teams():
        bst.insert(t)
    assert len(bst.inorder()) == 4


def test_empty_bst_inorder():
    bst = BST()
    assert bst.inorder() == []


def test_single_team():
    bst = BST()
    t = Team("Solo")
    t.wins = 8
    bst.insert(t)
    result = bst.inorder()
    assert len(result) == 1
    assert result[0].name == "Solo"


def test_bst_rebuilt_after_wins_change():
    """BST is rebuilt from scratch each week — verify fresh insert works."""
    bst = BST()
    teams = make_teams()
    teams[0].wins = 14  # now Alpha has the most
    for t in teams:
        bst.insert(t)
    result = bst.inorder()
    assert result[0].name == "Alpha"
