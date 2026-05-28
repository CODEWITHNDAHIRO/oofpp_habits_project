from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class Periodicity(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Habit:
    name: str
    description: str
    periodicity: Periodicity
    starting_at: datetime = field(default_factory=datetime.now)
    completions: List[datetime] = field(default_factory=list)
    habit_id: Optional[int] = field(default=None, compare=False)

    def check_off(self, at=None):
        ts = at or datetime.now()
        self.completions.append(ts)
        self.completions.sort()
        return ts

    def __str__(self):
        return (
            f"Habit(name={self.name}, "
            f"periodicity={self.periodicity.value}, "
            f"completions={len(self.completions)})"
        )