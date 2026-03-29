# tests/test_graph.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ds_engine import ScheduleGraph

TEAMS = ["Alpha", "Beta", "Gamma", "Delta"]


def make_graph():
    g = ScheduleGraph()
    g.add_matchup("Alpha", "Beta")
    g.add_matchup("Alpha", "Gamma")
    g.add_matchup("Beta",  "Delta")
    g.add_matchup("Gamma", "Delta")
    return g


def test_bfs_finds_direct_connection():
    g = make_graph()
    path = g.bfs("Alpha", "Beta")
    assert path == ["Alpha", "Beta"]


def test_bfs_finds_two_hop_path():
    g = make_graph()
    # Alpha-Beta-Delta or Alpha-Gamma-Delta
    path = g.bfs("Alpha", "Delta")
    assert path[0] == "Alpha"
    assert path[-1] == "Delta"
    assert len(path) == 3


def test_bfs_same_node_returns_single():
    g = make_graph()
    path = g.bfs("Alpha", "Alpha")
    assert path == ["Alpha"]


def test_bfs_unreachable_returns_empty():
    g = ScheduleGraph()
    g.add_matchup("Alpha", "Beta")
    g.add_matchup("Gamma", "Delta")
    path = g.bfs("Alpha", "Delta")
    assert path == []


def test_dfs_visits_all_connected_nodes():
    g = make_graph()
    path = g.dfs("Alpha")
    assert set(path) == set(TEAMS)


def test_dfs_no_duplicates():
    g = make_graph()
    path = g.dfs("Alpha")
    assert len(path) == len(set(path))
