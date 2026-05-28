from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import list, Optional
from enum import Enum

class Periodicity(str,Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'

@dataclass
class Habit:
    name: str
    periodicity: Periodicity
    starting_date: datetime = field(default_factory=datetime.now)
    ending_date: list[datetime] = field(default_factory=list)
    completions: List[datetime] = field(default=None, compare=False)

    def check_off(self, at=None):
        ts = at or datetime.now()
        self.completions.append(ts)
        self.completions.sort()
        return ts
    
    def __str__(self):
        return (f"Habit(name={self.name},"
                f"periodicity={self.periodicity.value},"
                f"completions={len(self.completions)})")