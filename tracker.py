from habit import Habit

class HabitTracker:
    """
    Manages multiple habits.
    """

    def __init__(self):
        self.habits = []

    def add_habit(self, name, periodicity, description=""):
        habit = Habit(name, periodicity, description)
        self.habits.append(habit)
        return habit

    def list_habits(self, periodicity=None):
        if periodicity:
            return [h for h in self.habits if h.periodicity == periodicity]
        return self.habits

    def delete_habit(self, name):
        self.habits = [h for h in self.habits if h.name != name]
