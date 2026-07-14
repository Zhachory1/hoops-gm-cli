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
        # Initialize the two hash-table dictionaries
        self.players_ids = {}
        self.players_names = {}

    def load(self, player: Player) -> None:
        # Insert the player into both dicts
        self.players_ids[player.id] = player
        self.players_names[player.name.lower()] = player

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        # Return the Player with this id, or None if not found
        return self.players_ids.get(player_id, None)

    def get_player_by_name(self, name: str) -> Optional[Player]:
        # Return the Player with this name (case-insensitive), or None
        return self.players_names.get(name.lower(), None)

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


def run_snake_draft(teams: List[Team], available: List[Player], user_team: Optional[Team] = None) -> None:
    """
    Snake draft: round 1 picks team 1→N, round 2 picks N→1, alternating.

    STUDENT TASK: Implement this function using your Queue and Stack above.
    Requirements:
      - Use a Queue to manage the current round's pick order
      - Reverse the Queue order on every even round (snake behavior)
      - Use a Stack to record each pick so the user can type 'undo'
      - Print top 15 available players each turn
      - user_team picks interactively; all other teams auto-pick index 0
      - If user_team is None, all teams auto-pick (useful for testing)
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
def _is_lower_standing(team: Team, other: Team) -> bool:
    if team.wins != other.wins:
        return team.wins < other.wins
    if team.losses != other.losses:
        return team.losses > other.losses
    return team.name.lower() > other.name.lower()


class BSTNode:
    """Single node in the BST. Stores a Team and left/right child pointers."""

    def __init__(self, team: Team):
        self.team = team
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


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
        self._root: Optional[BSTNode] = None

    def insert(self, team: Team) -> None:
        self._root = self._insert(self._root, team)

    def _insert(self, node: Optional[BSTNode], team: Team) -> BSTNode:
        if node is None:
            return BSTNode(team)
        if _is_lower_standing(team, node.team):
            node.left = self._insert(node.left, team)
        else:
            node.right = self._insert(node.right, team)
        return node

    def inorder(self) -> List[Team]:
        """Return teams in descending standings order (1st place first)."""
        result: List[Team] = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: List[Team]) -> None:
        if node is None:
            return
        self._inorder(node.right, result)
        result.append(node.team)
        self._inorder(node.left, result)


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
    def team_score(team: Team, opponent: Team) -> int:
        assist_bonus = sum(player.assists_avg for player in team.roster) * 0.1
        defense_penalty = sum(player.defense_rating for player in opponent.roster) * 0.05
        total = 0.0
        for player in team.roster:
            mu = player.points_avg + assist_bonus - defense_penalty
            total += max(0.0, random.gauss(mu, 3.0))
        return int(round(total))

    score_a = team_score(team_a, team_b)
    score_b = team_score(team_b, team_a)
    winner = team_a if score_a >= score_b else team_b
    return winner, score_a, score_b
