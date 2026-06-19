from main import claim_waiver_player, parse_args
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
