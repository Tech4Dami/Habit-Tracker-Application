import sqlite3
import hashlib
from models import User, Habit
import datetime

DATABASE_NAME = "habit_tracker.db"


def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def create_tables(conn):
    """Creates the necessary tables for the application if they do not exist."""
    cursor = conn.cursor()
    # Users table to store user information and securely hashed passwords
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       user_id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       NOT
                       NULL
                       UNIQUE,
                       password
                       TEXT
                       NOT
                       NULL,
                       full_name
                       TEXT,
                       email
                       TEXT
                   );
                   """)
    # Habits table to store each habit, linked to a user
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS habits
                   (
                       habit_id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER
                       NOT
                       NULL,
                       name
                       TEXT
                       NOT
                       NULL,
                       periodicity
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TEXT
                       NOT
                       NULL,
                       is_active
                       INTEGER
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       user_id
                   ) ON DELETE CASCADE
                       );
                   """)
    # Completions table to log each completion for a habit
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS completions
                   (
                       completion_id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       habit_id
                       INTEGER
                       NOT
                       NULL,
                       timestamp
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       habit_id
                   ) REFERENCES habits
                   (
                       habit_id
                   ) ON DELETE CASCADE
                       );
                   """)
    conn.commit()


def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(conn, username, password, full_name, email):
    """
    Registers a new user with a hashed password.
    Returns True on success, False if the username already exists.
    """
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?)",
                       (username, hashed_password, full_name, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(conn, username, password):
    """
    Authenticates a user.
    Returns the user's ID on success, None on failure.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user and user['password'] == hash_password(password):
        return user['user_id']
    return None


def save_habit(conn, user_id, habit):
    """Saves a new habit for a specific user to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO habits (user_id, name, periodicity, created_at, is_active) VALUES (?, ?, ?, ?, ?)",
                   (user_id, habit.name, habit.periodicity, habit.created_at.isoformat(), 1))  # Use isoformat for date
    conn.commit()
    return cursor.lastrowid  # Return the new habit ID


def load_habits_for_user(conn, user_id):
    """
    Loads all habits for a given user from the database.
    Returns a list of Habit objects.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE user_id = ?", (user_id,))
    habits_data = cursor.fetchall()

    habits = []
    for row in habits_data:
        habit_id = row['habit_id']
        name = row['name']
        periodicity = row['periodicity']
        created_at = row['created_at']
        is_active = row['is_active']

        # Load all completions for this specific habit
        completions_cursor = conn.cursor()
        completions_cursor.execute("SELECT timestamp FROM completions WHERE habit_id = ? ORDER BY timestamp",
                                   (habit_id,))
        completions_data = completions_cursor.fetchall()

        # Convert completion timestamps to datetime objects
        completions = [datetime.datetime.fromisoformat(c['timestamp']) for c in completions_data]

        # The Habit constructor must accept 6 positional arguments plus self (total 7)
        habit = Habit(name, periodicity, habit_id, created_at, is_active, completions)
        habits.append(habit)

    return habits


def save_completion(conn, habit_id, timestamp):
    """Saves a completion for a habit to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO completions (habit_id, timestamp) VALUES (?, ?)",
                   (habit_id, timestamp.isoformat()))
    conn.commit()


def delete_habit(conn, habit_id):
    """Deletes a habit and all its associated completions from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
    conn.commit()


def delete_user(conn, user_id):
    """Deletes a user and all their habits and completions."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()


# --- New Function for Phase 2 Proof ---
def add_test_data(conn):
    """
    Creates a dedicated test user and populates the database with data
    spanning over 4 weeks to prove streak logic and persistence.
    """
    TEST_USER = "TestProofUser"
    TEST_PASS = "proof2025"

    # 1. Clear previous test data and ensure fresh tables
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (TEST_USER,))
        conn.commit()
    except Exception:
        pass  # Ignore if table doesn't exist yet

    # 2. Create Test User
    register_user(conn, TEST_USER, TEST_PASS, "Phase 2 Tester", "test@iu.edu")
    user_id = login_user(conn, TEST_USER, TEST_PASS)

    if not user_id:
        print("ERROR: Could not create or log in test user.")
        return None

    # 3. Define Habits and Logs for Proof (Start Date: 4 weeks ago)

    # Helper for date manipulation
    four_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=4)
    start_date = four_weeks_ago.replace(hour=12, minute=0, second=0, microsecond=0)

    # --- Daily Habit Proof: 5-Day Streak Broken by a Miss ---
    # Expected Streak: 5 (Miss breaks it before subsequent completions)
    daily_habit = Habit("Daily Reading", "daily", created_at=start_date)
    daily_id = save_habit(conn, user_id, daily_habit)

    daily_logs = [
        start_date + datetime.timedelta(days=i) for i in range(5)  # Streak of 5
    ]
    # Logs a completion 7 days later (missed Day 6)
    daily_logs.append(start_date + datetime.timedelta(days=7))
    daily_logs.append(start_date + datetime.timedelta(days=8))

    # --- Weekly Habit Proof: Perfect 4-Week Streak ---
    # Expected Streak: 4
    weekly_habit = Habit("Weekly Budget Review", "weekly", created_at=start_date)
    weekly_id = save_habit(conn, user_id, weekly_habit)

    # Logs one completion per week for 4 consecutive weeks
    weekly_logs = [
        start_date + datetime.timedelta(weeks=0, days=1),  # Week 1
        start_date + datetime.timedelta(weeks=1, days=2),  # Week 2
        start_date + datetime.timedelta(weeks=2, days=3),  # Week 3
        start_date + datetime.timedelta(weeks=3, days=0),  # Week 4
    ]

    # --- Other Habits (for the "5+ Habits" requirement) ---
    save_habit(conn, user_id, Habit("Evening Walk", "daily", created_at=start_date))
    save_habit(conn, user_id, Habit("Team Sync", "weekly", created_at=start_date))
    save_habit(conn, user_id, Habit("Skill Practice", "daily", created_at=start_date))

    # 4. Save all completions
    for log_date in daily_logs:
        save_completion(conn, daily_id, log_date)
    for log_date in weekly_logs:
        save_completion(conn, weekly_id, log_date)

    print(f"\n--- Test Data Setup Complete for user: {TEST_USER} ---")
    return user_id, TEST_USER, TEST_PASS
