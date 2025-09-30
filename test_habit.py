import pytest
import datetime
from habit import Habit
from fixtures import load_sample_habits
from analyzer import longest_streak, habits_by_periodicity, get_last_completion, calculate_streak, \
    habits_missed_last_week
import storage


# A fixture for a temporary in-memory database connection for testing
@pytest.fixture
def test_db_conn():
    conn = storage.get_db_connection(':memory:')  # Use in-memory DB for fast tests
    storage.create_tables(conn)
    yield conn
    conn.close()


# Test the core functionality of the Habit class
def test_habit_creation():
    """Test that a Habit object is created correctly."""
    h = Habit("Run", "daily")
    assert h.name == "Run"
    assert h.periodicity == "daily"
    assert h.is_active is True
    assert len(h.completions) == 0


def test_log_completion():
    """Test that completion is logged correctly."""
    h = Habit("Exercise", "daily")
    h.log_completion()
    assert len(h.completions) == 1
    assert isinstance(h.completions[0], datetime.datetime)


# Test the streak calculation logic from the analyzer module
def test_daily_streak_calculation():
    """Test streak calculation for a daily habit."""
    h = Habit("Read", "daily")
    today = datetime.datetime.now()
    # Log completions for a 5-day continuous streak
    for i in range(5):
        h.log_completion(today - datetime.timedelta(days=i))

    streak = calculate_streak(h.completions, h.periodicity)
    assert streak == 5


def test_weekly_streak_calculation():
    """Test streak calculation for a weekly habit."""
    h = Habit("Clean", "weekly")
    today = datetime.datetime.now()
    # Log completions for a 3-week continuous streak
    for i in range(3):
        h.log_completion(today - datetime.timedelta(weeks=i))

    streak = calculate_streak(h.completions, h.periodicity)
    assert streak == 3


def test_streak_with_gap():
    """Test that the streak calculation resets with a gap."""
    h = Habit("Meditate", "daily")
    today = datetime.datetime.now()
    # Log completions for a 3-day streak
    for i in range(3):
        h.log_completion(today - datetime.timedelta(days=i))
    # Log a completion after a 2-day gap
    h.log_completion(today - datetime.timedelta(days=5))

    streak = calculate_streak(h.completions, h.periodicity)
    # The longest streak should still be 3
    assert streak == 3


# Test the core analyzer functions
def test_habits_by_periodicity(test_db_conn):
    """Test filtering habits by periodicity."""
    habits = load_sample_habits(test_db_conn, num_daily=5, num_weekly=5, num_weeks=1)
    daily_habits = habits_by_periodicity(habits, 'daily')
    assert len(daily_habits) == 5
    weekly_habits = habits_by_periodicity(habits, 'weekly')
    assert len(weekly_habits) == 5


def test_longest_streak_from_database(test_db_conn):
    """Test overall longest streak using data from the database."""
    # This loads and populates the database with 50 continuous habits
    habits = load_sample_habits(test_db_conn)
    # The longest streak should be at least 28 (4 weeks * 7 days)
    assert longest_streak(habits) >= 28


def test_habits_missed_last_week_with_data(test_db_conn):
    """
    Test the habits missed function with a known missed habit.
    This creates a clean test case by saving a habit with an old completion.
    """
    # Create a habit that has been missed for more than a week
    missed_habit = Habit("Old Habit", "daily")
    missed_habit.log_completion(datetime.datetime.now() - datetime.timedelta(days=10))
    storage.save_habit(test_db_conn, missed_habit)

    # Load all habits from the database, including our old habit
    habits = storage.load_all_habits(test_db_conn)

    # Check if the function correctly identifies the missed habit
    missed = habits_missed_last_week(habits)
    assert len(missed) == 1
    assert missed[0].name == "Old Habit"