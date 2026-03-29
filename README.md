# Terminal Hoops GM

A terminal-based fantasy basketball game used as a teaching tool for Data Structures & Algorithms. You manage a team through a snake draft, weekly matchups, and a 14-week season — all powered by DS&A implementations you write yourself.

---

## Quickstart

```bash
python3 main.py
```

You'll be prompted to name your team, draft your roster, then manage your season week by week.

---

## Your Job: Implement `ds_engine.py`

All game logic lives in `ds_engine.py`. Every class and function is stubbed out with a `TODO` and raises `NotImplementedError`. **Your task is to replace each stub with a working implementation.**

The game will not run until you implement the modules. Use the test suite to check your work as you go.

### Module 1 — Hash Table: `PlayerDatabase`

**File:** `ds_engine.py` | **Tests:** `tests/test_player_database.py`

Build a player lookup system backed by two dictionaries — one keyed by player ID, one by player name. Both lookups must be O(1).

| Method | Description |
|---|---|
| `load(player)` | Insert a player into both dicts |
| `get_player_by_id(id)` | Return the player, or `None` |
| `get_player_by_name(name)` | Case-insensitive lookup, or `None` |

---

### Module 2 — Queue, Stack & Snake Draft: `Queue`, `Stack`, `run_snake_draft`

**File:** `ds_engine.py` | **Tests:** `tests/test_draft.py`

Implement a FIFO **Queue** and a LIFO **Stack** using Python lists, then use both to power the snake draft.

**Queue** — draft turn order:
- `enqueue(item)` / `dequeue()` / `is_empty()` / `size()` / `__iter__`

**Stack** — undo history:
- `push(item)` / `pop()` / `peek()` / `is_empty()`

**`run_snake_draft(teams, available, user_team=None)`** — the draft engine:
- Use a Queue for the current round's pick order
- Reverse the Queue every even round (snake behavior)
- Use a Stack so the user can type `undo` to take back the last pick
- Display available players in a table each turn
- `user_team` picks interactively; all others auto-pick from the pool
- If `user_team is None`, all teams auto-pick (used by the test suite)

---

### Module 3 — Max-Heap: `MaxHeap`

**File:** `ds_engine.py` | **Tests:** `tests/test_heap.py`

An array-backed binary max-heap ordered by `Player.fantasy_value`. Powers the waiver wire — the best available free agent is always at the top.

| Method | Description |
|---|---|
| `insert(player)` | Append and sift up |
| `extract_max()` | Swap root with last, pop, sift down, return max |
| `_sift_up(i)` | Bubble index `i` upward until heap property holds |
| `_sift_down(i)` | Push index `i` downward until heap property holds |

Index math:
```
parent(i)      = (i - 1) // 2
left_child(i)  = 2*i + 1
right_child(i) = 2*i + 2
```

---

### Module 4 — Merge Sort: `merge_sort`

**File:** `ds_engine.py` | **Tests:** `tests/test_sort.py`

Recursive O(n log n) sort returning players in **descending** order by a given stat key (`'points_avg'`, `'assists_avg'`, `'defense_rating'`). Must not mutate the input list.

```python
merge_sort(players, key)   # recursive split + merge
_merge(left, right, key)   # merge two sorted-descending lists into one
```

---

### Module 5 — Binary Search Tree: `BST`

**File:** `ds_engine.py` | **Tests:** `tests/test_bst.py`

A BST ordered by `Team.wins` used to maintain league standings. Left subtree = fewer wins, right subtree = more wins. A right→node→left in-order traversal produces the standings in descending win order.

| Method | Description |
|---|---|
| `insert(team)` | Place team at the correct BST position |
| `_insert(node, team)` | Recursive helper — returns the (possibly new) node |
| `inorder()` | Return teams in descending win order |
| `_inorder(node, result)` | Recursive traversal helper |

Also implement `BSTNode.__init__` to store `team`, `left`, and `right`.

---

### Module 6 — Graph (BFS & DFS): `ScheduleGraph`

**File:** `ds_engine.py` | **Tests:** `tests/test_graph.py`

An undirected adjacency-list graph where nodes are team names and edges are scheduled matchups. Used to explore schedule connections.

| Method | Description |
|---|---|
| `add_matchup(a, b)` | Add both teams as nodes; connect them as neighbors |
| `bfs(start, end)` | Shortest path between two teams — use your Queue |
| `dfs(start)` | All teams reachable from start — implement recursively |

---

### Module 7 — Game Simulator: `simulate_matchup`

**File:** `ds_engine.py` | **Tests:** `tests/test_simulator.py`

Stochastic matchup simulator using a Gaussian distribution. For each player:

```
mu    = player.points_avg + assist_bonus - defense_penalty
score = max(0, gauss(mu, sigma=3.0))
```

Where:
- `assist_bonus`    = team's total `assists_avg × 0.1`
- `defense_penalty` = opponent's total `defense_rating × 0.05`

Sum all player scores per team, return `(winner, score_a, score_b)`.

---

## Running the Tests

Run all tests:
```bash
python3 -m pytest tests/
```

Run a specific module:
```bash
python3 -m pytest tests/test_player_database.py  # Module 1
python3 -m pytest tests/test_draft.py            # Module 2
python3 -m pytest tests/test_heap.py             # Module 3
python3 -m pytest tests/test_sort.py             # Module 4
python3 -m pytest tests/test_bst.py              # Module 5
python3 -m pytest tests/test_graph.py            # Module 6
python3 -m pytest tests/test_simulator.py        # Module 7
```

A fully correct implementation passes all 38 tests.

---

## Project Structure

```
hoops-gm-cli/
├── ds_engine.py        ← implement everything here
├── main.py             ← game loop (do not modify)
├── models.py           ← Player and Team dataclasses (do not modify)
├── data/
│   └── players.json    ← 3,500+ real NBA players
└── tests/
    ├── test_player_database.py
    ├── test_draft.py
    ├── test_heap.py
    ├── test_sort.py
    ├── test_bst.py
    ├── test_graph.py
    └── test_simulator.py
```

---

## Fantasy Value Formula

Player value used throughout the game:

```
fantasy_value = points_avg + (assists_avg × 1.5) + (defense_rating × 2.0)
```

Only players with `fantasy_value ≥ 5` are included in the player pool.
