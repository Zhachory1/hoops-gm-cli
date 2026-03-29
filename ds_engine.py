# ds_engine.py
# All Data Structures & Algorithms implementations live here.
# Each class/function below is a stub — YOUR job is to implement it.
# Run the tests in tests/ to verify your implementations are correct.

import random
from models import Player, Team
from typing import List, Optional


# ── Module 1: Hash Table ──────────────────────────────────────────────────────
class PlayerDatabase:
    """
    O(1) player lookup by ID or name.

    STUDENT TASK: Implement this class using two dictionaries as your
    hash tables — one keyed by player ID, one keyed by player name.
    See tests/test_player_database.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize your two hash-table dicts here
        pass

    def load(self, player: Player) -> None:
        # TODO: Insert the player into both dicts
        raise NotImplementedError

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        # TODO: Return the Player with this id, or None if not found
        raise NotImplementedError

    def get_player_by_name(self, name: str) -> Optional[Player]:
        # TODO: Return the Player with this name (case-insensitive), or None
        raise NotImplementedError


# ── Module 2: Draft Room ──────────────────────────────────────────────────────
class Queue:
    """
    FIFO queue for managing draft turn order.

    STUDENT TASK: Implement using a Python list as internal storage.
    enqueue adds to the back; dequeue removes from the front.
    See tests/test_draft.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize internal storage
        pass

    def enqueue(self, item) -> None:
        # TODO: Add item to the back of the queue
        raise NotImplementedError

    def dequeue(self):
        # TODO: Remove and return item from the front; return None if empty
        raise NotImplementedError

    def is_empty(self) -> bool:
        # TODO: Return True if queue has no items
        raise NotImplementedError

    def size(self) -> int:
        # TODO: Return the number of items
        raise NotImplementedError

    def __iter__(self):
        # TODO: Allow iteration over items (needed by run_snake_draft)
        raise NotImplementedError


class Stack:
    """
    LIFO stack for draft undo history.

    STUDENT TASK: Implement using a Python list as internal storage.
    push and pop both operate on the same end.
    See tests/test_draft.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize internal storage
        pass

    def push(self, item) -> None:
        # TODO: Add item to the top
        raise NotImplementedError

    def pop(self):
        # TODO: Remove and return top item; return None if empty
        raise NotImplementedError

    def peek(self):
        # TODO: Return top item without removing; return None if empty
        raise NotImplementedError

    def is_empty(self) -> bool:
        # TODO: Return True if stack has no items
        raise NotImplementedError


def run_snake_draft(teams: List[Team], available: List[Player]) -> None:
    """
    Snake draft: round 1 picks team 1→4, round 2 picks 4→1, alternating.

    STUDENT TASK: Implement this function using your Queue and Stack above.
    Requirements:
      - Use a Queue to manage the current round's pick order
      - Reverse the Queue order on every even round (snake behavior)
      - Use a Stack to record each pick so the user can type 'undo'
      - Print top 15 available players each turn
      - Prompt the player by number; CPU teams pick index 0 automatically
    See tests/test_draft.py for integration tests.
    """
    # TODO: Implement snake draft here
    raise NotImplementedError


# ── Module 3: Waiver Wire ─────────────────────────────────────────────────────
class MaxHeap:
    """
    Array-backed binary max-heap ordered by Player.fantasy_value.

    STUDENT TASK: Implement using a list with sift-up and sift-down.
    Index math:
      parent(i)      = (i - 1) // 2
      left_child(i)  = 2*i + 1
      right_child(i) = 2*i + 2
    See tests/test_heap.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize internal list
        pass

    def insert(self, player: Player) -> None:
        # TODO: Append and sift up
        raise NotImplementedError

    def extract_max(self) -> Optional[Player]:
        # TODO: Swap root with last, pop, sift down, return the max
        raise NotImplementedError

    def _sift_up(self, i: int) -> None:
        # TODO: Bubble item at index i upward until heap property holds
        raise NotImplementedError

    def _sift_down(self, i: int) -> None:
        # TODO: Push item at index i downward until heap property holds
        raise NotImplementedError


# ── Module 4: Stat Leaderboards ───────────────────────────────────────────────
def merge_sort(players: List[Player], key: str) -> List[Player]:
    """
    Recursive merge sort returning players in DESCENDING order by `key`.

    STUDENT TASK: Implement a recursive O(n log n) merge sort.
    Must NOT mutate the input list.
    `key` is a Player attribute name (e.g. 'points_avg', 'assists_avg').
    See tests/test_sort.py for the expected interface.
    """
    # TODO: Base case + recursive split + merge
    raise NotImplementedError


def _merge(left: List[Player], right: List[Player], key: str) -> List[Player]:
    """
    Merge two sorted (descending) lists into one sorted (descending) list.

    STUDENT TASK: Implement the merge step used by merge_sort.
    """
    # TODO: Two-pointer merge — pick the larger value first
    raise NotImplementedError


# ── Module 5: League Standings ────────────────────────────────────────────────
class BSTNode:
    """Single node in the BST. Stores a Team and left/right child pointers."""

    def __init__(self, team: Team):
        # TODO: Store the team; set left and right to None
        raise NotImplementedError


class BST:
    """
    Binary Search Tree ordered by Team.wins.
    Left subtree  → fewer wins than parent
    Right subtree → more wins than parent
    In-order traversal right→left gives descending win order.

    STUDENT TASK: Implement insert and inorder traversal.
    See tests/test_bst.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize root to None
        pass

    def insert(self, team: Team) -> None:
        # TODO: Insert team into the correct BST position by wins
        raise NotImplementedError

    def _insert(self, node: Optional[BSTNode], team: Team) -> BSTNode:
        # TODO: Recursive helper — return the (possibly new) node
        raise NotImplementedError

    def inorder(self) -> List[Team]:
        """Return teams in descending win order (1st place first)."""
        # TODO: Traverse right→node→left and collect teams
        raise NotImplementedError

    def _inorder(self, node: Optional[BSTNode], result: List[Team]) -> None:
        # TODO: Recursive helper for inorder traversal
        raise NotImplementedError


# ── Module 6: Schedule Network ────────────────────────────────────────────────
class ScheduleGraph:
    """
    Undirected adjacency-list graph. Nodes = team names, edges = matchups.

    STUDENT TASK: Implement BFS (shortest path) and DFS (full road trip).
    See tests/test_graph.py for the expected interface.
    """

    def __init__(self):
        # TODO: Initialize adjacency dict: { team_name: [neighbor, ...] }
        pass

    def _add_node(self, name: str) -> None:
        # TODO: Add node if not already present
        raise NotImplementedError

    def add_matchup(self, team_a: str, team_b: str) -> None:
        # TODO: Add both teams as nodes; append each to the other's list
        raise NotImplementedError

    def bfs(self, start: str, end: str) -> List[str]:
        """
        Return shortest path from start to end as a list of team names.
        Return [] if unreachable. Return [start] if start == end.

        STUDENT TASK: Use your Queue for the frontier. Track visited nodes
        to avoid cycles.
        """
        # TODO: BFS with path tracking
        raise NotImplementedError

    def dfs(self, start: str) -> List[str]:
        """
        Return all nodes reachable from start via depth-first traversal.
        No duplicates.

        STUDENT TASK: Implement recursively using a visited set.
        """
        # TODO: Kick off recursive DFS
        raise NotImplementedError

    def _dfs_recursive(self, node: str, visited: set, result: List[str]) -> None:
        # TODO: Mark visited, append to result, recurse on unvisited neighbors
        raise NotImplementedError


# ── Module 7: Game Simulator ──────────────────────────────────────────────────
def simulate_matchup(team_a: Team, team_b: Team) -> tuple:
    """
    Stochastic matchup simulator using Gaussian (normal) distribution.

    STUDENT TASK: For each player, compute an adjusted score using
    random.gauss(mu, sigma) where:
      mu = player.points_avg + assist_bonus - defense_penalty
      assist_bonus    = team's total assists_avg * 0.1
      defense_penalty = opponent's total defense_rating * 0.05
      sigma = 3.0

    Floor individual scores at 0. Sum all player scores per team.
    Return (winner: Team, score_a: int, score_b: int).
    See tests/test_simulator.py for the expected interface.
    """
    # TODO: Compute team scores, determine winner, return tuple
    raise NotImplementedError
