import pytest
from datetime import datetime, timedelta
from habit import Habit, Periodicity

#helpers
def make_habit(name="Test", periodicity=Periodicity.DAILY, days_ago=10):
   """ creating a habit with a creation date in the past """
   return Habit(
      name=name,
      description="Test habit",
      periodicity=periodicity,
      created_at=datetime.now() - timedelta(days=days_ago),

   )

# tests
def test_habit_name():
    h = make_habit(name="Exercise")
    assert h.name == "Exercise"
   
def test_habit_description():
    h = Habit("make bed", "Make your bed every morning", Periodicity.DAILY)
    assert h.description == "Make your bed every morning"

def test_habit_default_no_completions():
    h = make_habit()
    assert h.completions == []

def test_habit_id_defaults_to_none():
    h = make_habit()
    assert h.habit_id is None

def test_periodicity_daily():
    h = make_habit(periodicity=Periodicity.DAILY)
    assert h.periodicity == Periodicity.DAILY

def test_periodicity_weekly():
    h = make_habit(periodicity=Periodicity.WEEKLY)
    assert h.periodicity == Periodicity.WEEKLY

# test check_off adds a completion timestamp

def test_check_off_adds_completion():
    h = make_habit()
    h.check_off()
    assert len(h.completions) == 1

def test_check_off_returns_timestamp():
    h = make_habit()
    ts = h.check_off()
    assert isinstance(ts, datetime)

def test_check_off_with_explicit_time():
    h = make_habit()
    explicit = datetime(2024, 1, 15, 8, 0, 0)
    h.check_off(at=explicit)
    assert h.completions[0] == explicit


def test_check_off_multiple_sorted():
    h = make_habit()
    t2 = datetime(2024, 1, 2)
    t1 = datetime(2024, 1, 1)
    h.check_off(at=t2)
    h.check_off(at=t1)
    assert h.completions[0] == t1
    assert h.completions[1] == t2

#current streak tests

def test_current_streak_no_completions():
   h = make_habit()
   assert h.current_streak() == 0

def test_current_streak_today_only():
   h = make_habit()
   h.check_off(at=datetime.now())
   assert h.current_streak() == 1

def test_current_streak_three_days():
   h = make_habit()
   for days_ago in [2, 1, 0]:
       h.check_off(at=datetime.now() - timedelta(days=days_ago))
   assert h.current_streak() == 3
   
def test_current_streak_broken_yesterday():
   h = make_habit()
   h.check_off(at=datetime.now() -timedelta(days=2))
   h.check_off(at=datetime.now())
   # any gap on day 1 should break the streak
   assert h.current_streak() == 1

# longest streak tests

def test_longest_streak_no_completions():
    h = make_habit()
    assert h.longest_streak() == 0

def test_longest_streak_perfect_week():
    h = make_habit(days_ago=7)
    for i in range(7):
        h.check_off(at=datetime.now() - timedelta(days=6 - i))
    assert h.longest_streak() == 7

def test_longest_streak_with_gap():
    h = make_habit(days_ago=10)
   # Days 10,9,8 ago - gap - days 5,4,3,2,1,0 ago
    for  days_ago in [10, 9, 8, 5, 4, 3, 2, 1, 0]:
       h.check_off(at=datetime.now() - timedelta(days=days_ago))
    assert h.longest_streak() == 6

# is_broken_today tests

def test_not_broken_if_completed_today():
    h = make_habit()
    h.check_off(at=datetime.now())
    assert h.is_broken_today() == False

def test_broken_if_no_completion_today():
    h = make_habit(days_ago=5)
    h.check_off(at=datetime.now() - timedelta(days=3))
    assert h.is_broken_today() is True

def test_not_broken_on_creation_day():
   # brand new habit - same period as creation , not yet broken
    h = Habit("New", "new", Periodicity.DAILY)
    assert h.is_broken_today() is False

#weekly habit tests

def test_weekly_streak_one_week():
    h = make_habit(periodicity=Periodicity.WEEKLY, days_ago=14)
    h.check_off(at=datetime.now() - timedelta(days=3))
    h.check_off(at=datetime.now())
    assert h.current_streak() >= 1

def test_weekly_longest_streak():
  #pin creation date to a fixed Monday to avoid week boundary issues
    fixed_start = datetime(2026, 5, 4, 0, 0, 0) # monday may 4, 2026
    h = Habit(
       name = "weekly Test",
       description = "Test weekly habit",
       periodicity=Periodicity.WEEKLY,
       created_at=fixed_start,
    )
    # Check off on Tuesday of each of the 4 weeks
    h.check_off(at=datetime(2026, 5, 5))   # week 1 - Tuesday
    h.check_off(at=datetime(2026, 5, 12))  # week 2 - Tuesday
    h.check_off(at=datetime(2026, 5, 19))  # week 3 - Tuesday
    h.check_off(at=datetime(2026, 5, 26))  # week 4 - Tuesday
    assert h.longest_streak() == 4
    