import datetime

class Habit:
    """
    Class representing a habit, including its properties and a list of completions.
    """

    def __init__(self, name, periodicity, description="", created_at=None, is_active=True):
        """
        Initializes a Habit object.

        Args:
            name (str): The name of the habit (e.g., "Go for a walk").
            periodicity (str): How often the habit should be tracked ("daily" or "weekly").
            description (str, optional): A brief description of the habit. Defaults to "".
            created_at (datetime.datetime, optional): The timestamp when the habit was created. Defaults to now.
            is_active (bool, optional): The active status of the habit. Defaults to True.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity.lower()
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.is_active = is_active
        self.completions = []  # A list to store completion timestamps

    def log_completion(self, timestamp=None):
        """
        Logs a completion for the habit with a specific timestamp.
        """
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.completions.append(timestamp)

    def get_last_completion(self):
        """
        Returns the timestamp of the last completion.
        This is a helper for the CLI to display information.
        """
        if self.completions:
            return max(self.completions)
        return None

    def __repr__(self):
        """
        Returns a string representation of the Habit object.
        """
        return f"Habit(name='{self.name}', periodicity='{self.periodicity}', is_active={self.is_active})"