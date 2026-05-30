from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date ,timedelta
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
    created_at: datetime = field(default_factory=datetime.now)
    completions: List[datetime] = field(default_factory=list)
    habit_id: Optional[int] = field(default=None, compare=False)


    def check_off(self, at=None):
        ts = at or datetime.now()
        self.completions.append(ts)
        self.completions.sort()
        return ts
    def _period_start(self, dt: date) -> date:
        if self.periodicity == Periodicity.DAILY:
            return dt
        return dt - timedelta(days=dt.weekday())
    
    def _was_completed_in_period(self, period_start: date) -> bool:
        dates = [c.date() for c in self.completions]
        if self.periodicity == Periodicity.DAILY:
            return period_start in dates
        return any(
            self. _period_start(d) == period_start for d in dates
        )
    def _periods_between( self, start: date, end: date) -> list:
        periods = []
        delta = timedelta( days=1 if self.periodicity == Periodicity.DAILY else 7)
        current = self._period_start(start)
        stop = self._period_start(end)
        while current <= stop:
            periods.append(current)
            current += delta
        return periods
    def current_streak(self) -> int:
        if not self.completions:
            return 0
        today = date.today()
        streak = 0
        delta = timedelta(days=1 if self.periodicity == Periodicity.DAILY else 7)
        period = self._period_start(today)
        while True:
            if self._was_completed_in_period(period):
                streak += 1
                period -= delta
            else:
                break
        return streak
    def longest_streak(self) -> int:
        if not self.completions:
            return 0
        start = self._period_start(self.created_at.date())
        end = self._period_start(date.today())
        periods = self._periods_between(start,end)
        best = 0
        current = 0
        for p in periods:
            if self._was_completed_in_period(p):
                current += 1
                best = max(best, current)
            else:
                current = 0
        return best
    def is_broken_today(self) -> bool:
        today = date.today()
        current_period = self._period_start(today)
        creation_period = self._period_start(self.created_at.date())
        if current_period == creation_period:
            return False
        return not self._was_completed_in_period(current_period)

                     
    def __str__(self):
        return (
            f"Habit(name={self.name}, "
            f"periodicity={self.periodicity.value}, "
            f"completions={len(self.completions)})"
        )