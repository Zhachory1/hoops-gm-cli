import csv
import json

from main import export_summary_csv, export_summary_json, save_league_state, claim_waiver_player, parse_args
from models import Player, Team


def player(name, value):
    return Player(id=name, name=name, points_avg=value, assists_avg=0, defense_rating=0)


class FakeWire:
    def __init__(self):
        self.inserted = []

    def insert(self, player):
        self.inserted.append(player)


def test_parse_args_seed_and_weeks():
    args = parse_args(["--seed", "42", "--weeks", "3"])

    assert args.seed == 42
    assert args.weeks == 3


def test_parse_args_persistence_paths():
    args = parse_args(["--save", "state.json", "--export-json", "summary.json", "--export-csv", "summary.csv"])

    assert args.save == "state.json"
    assert args.export_json == "summary.json"
    assert args.export_csv == "summary.csv"


def test_invalid_waiver_drop_does_not_pop_roster():
    team = Team("User", roster=[player("A", 1), player("B", 2)])
    wire = FakeWire()
    top = player("Top", 10)

    assert claim_waiver_player(team, wire, top, "99") is False
    assert [p.name for p in team.roster] == ["A", "B"]
    assert [p.name for p in wire.inserted] == ["Top"]


def test_valid_waiver_drop_swaps_player():
    team = Team("User", roster=[player("A", 1), player("B", 2)])
    wire = FakeWire()
    top = player("Top", 10)

    assert claim_waiver_player(team, wire, top, "1") is True
    assert [p.name for p in team.roster] == ["B", "Top"]
    assert [p.name for p in wire.inserted] == ["A"]


def test_save_league_state_writes_json(tmp_path):
    user = Team("User", roster=[player("A", 1)], wins=1)
    cpu = Team("CPU", losses=1)
    result = {"week": 1, "team_a": "User", "team_b": "CPU", "score_a": 90, "score_b": 80, "winner": "User"}
    path = tmp_path / "state" / "league.json"

    save_league_state(str(path), [user, cpu], 2, 3, user, [result])

    payload = json.loads(path.read_text())
    assert payload["week"] == 2
    assert payload["total_weeks"] == 3
    assert payload["user_team"] == "User"
    assert payload["teams"][0]["roster"][0]["name"] == "A"
    assert payload["results"] == [result]


def test_export_summary_json_writes_draft_and_results(tmp_path):
    user = Team("User", roster=[player("A", 1)])
    result = {"week": 1, "team_a": "User", "team_b": "CPU", "score_a": 90, "score_b": 80, "winner": "User"}
    path = tmp_path / "summary.json"

    export_summary_json(str(path), [user], [result], user)

    payload = json.loads(path.read_text())
    assert payload["user_team"] == "User"
    assert payload["draft"][0]["name"] == "User"
    assert payload["draft"][0]["roster"][0]["name"] == "A"
    assert payload["results"] == [result]


def test_export_summary_csv_writes_draft_and_results_rows(tmp_path):
    user = Team("User", roster=[player("A", 1)])
    result = {"week": 1, "team_a": "User", "team_b": "CPU", "score_a": 90, "score_b": 80, "winner": "User"}
    path = tmp_path / "summary.csv"

    export_summary_csv(str(path), [user], [result])

    rows = list(csv.DictReader(path.open()))
    assert rows[0]["section"] == "draft"
    assert rows[0]["team"] == "User"
    assert rows[0]["player"] == "A"
    assert rows[1]["section"] == "result"
    assert rows[1]["week"] == "1"
    assert rows[1]["winner"] == "User"
