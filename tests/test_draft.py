# tests/test_draft.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Player, Team
from ds_engine import Queue, Stack, run_snake_draft

P = lambda n: Player(f"p{n:03d}", f"Player {n}", float(n), float(n)/3, float(n)/4)
TEAMS = [Team(f"Team {i}") for i in range(7)]
PLAYERS = [P(i) for i in range(1, 106)]  # 7 teams × 15 players


# ── Queue tests ───────────────────────────────────────────────────────────────

def test_queue_enqueue_dequeue_order():
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    assert q.dequeue() == "A"
    assert q.dequeue() == "B"


def test_queue_is_empty():
    q = Queue()
    assert q.is_empty()
    q.enqueue(1)
    assert not q.is_empty()


def test_queue_dequeue_empty_returns_none():
    q = Queue()
    assert q.dequeue() is None


def test_queue_size():
    q = Queue()
    for i in range(5):
        q.enqueue(i)
    assert q.size() == 5


# ── Stack tests ───────────────────────────────────────────────────────────────

def test_stack_push_pop_lifo():
    s = Stack()
    s.push("first")
    s.push("second")
    assert s.pop() == "second"
    assert s.pop() == "first"


def test_stack_is_empty():
    s = Stack()
    assert s.is_empty()
    s.push(99)
    assert not s.is_empty()


def test_stack_pop_empty_returns_none():
    s = Stack()
    assert s.pop() is None


# ── Snake draft integration tests ─────────────────────────────────────────────

def test_snake_draft_fills_all_rosters():
    teams = [Team(f"Team {i}") for i in range(7)]
    players = [P(i) for i in range(1, 106)]
    run_snake_draft(teams, players)
    for t in teams:
        assert len(t.roster) == 15


def test_snake_draft_no_duplicate_players():
    teams = [Team(f"Team {i}") for i in range(7)]
    players = [P(i) for i in range(1, 106)]
    run_snake_draft(teams, players)
    all_drafted = [p.id for t in teams for p in t.roster]
    assert len(all_drafted) == len(set(all_drafted))
