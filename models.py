import datetime


class User:
    """Represents a user in the system."""

    def __init__(self, username, full_name, email, user_id=None):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.email = email


class Habit:
    """Represents a habit with its name, periodicity, and completion history."""

    def __init__(self, name, periodicity, habit_id=None, created_at=None, is_active=True, completions=None):
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity

        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            # Handle cases where created_at is a string from the database
            if isinstance(created_at, str):
                self.created_at = datetime.datetime.fromisoformat(created_at)
            else:
                self.created_at = created_at

        self.is_active = is_active
        self.completions = completions if completions is not None else []
