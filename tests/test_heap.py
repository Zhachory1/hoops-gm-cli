# tests/test_heap.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Player
from ds_engine import MaxHeap


def p(pts, ast, dfn, pid="x"):
    return Player(pid, f"Player_{pts}", pts, ast, dfn)


def test_extract_max_returns_highest_fv():
    h = MaxHeap()
    # FV = pts + ast*1.5 + dfn*2.0
    low  = p(10, 1, 1)   # FV = 13.5
    mid  = p(20, 2, 2)   # FV = 27.0
    high = p(30, 5, 5)   # FV = 47.5
    for player in [low, mid, high]:
        h.insert(player)
    assert h.extract_max().points_avg == 30


def test_heap_empty_returns_none():
    h = MaxHeap()
    assert h.extract_max() is None


def test_insert_after_extract():
    h = MaxHeap()
    h.insert(p(20, 2, 2))   # FV = 27
    h.extract_max()
    h.insert(p(15, 1, 1))   # FV = 17.5
    result = h.extract_max()
    assert result is not None
    assert result.points_avg == 15


def test_heap_property_maintained_after_many_inserts():
    import random
    h = MaxHeap()
    players = [p(random.randint(8, 35), random.uniform(1, 12), random.uniform(3, 9)) for _ in range(30)]
    for player in players:
        h.insert(player)
    results = []
    while True:
        top = h.extract_max()
        if top is None:
            break
        results.append(top.fantasy_value)
    # Must be in descending order
    assert results == sorted(results, reverse=True)
