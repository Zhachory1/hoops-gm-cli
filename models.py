# models.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class Player:
    id: str
    name: str
    points_avg: float
    assists_avg: float
    defense_rating: float

    @property
    def fantasy_value(self) -> float:
        return self.points_avg + (self.assists_avg * 1.5) + (self.defense_rating * 2.0)


@dataclass
class Team:
    name: str
    roster: List[Player] = field(default_factory=list)
    wins: int = 0
    losses: int = 0

    MAX_ROSTER_SIZE = 15
