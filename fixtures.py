import datetime
import random
import storage
from habit import Habit


def load_complex_test_data(conn, num_habits=1000):
    """
    Creates and saves a complex set of up to 1000 habits with varied
    completion data to the database for realistic testing.

    Args:
        conn: The database connection object.
        num_habits (int): The total number of habits to create.
    """
    print(f"Generating and saving a complex test dataset of {num_habits} habits...")

    daily_habits_list = [
        "Read 10 pages", "Meditate for 5 min", "Drink 8 glasses of water",
        "Exercise for 30 min", "Write in a journal", "Learn a new language",
        "Practice coding", "Cook at home", "Walk the dog", "Take a vitamin",
        "Listen to a podcast", "Wake up early", "Stretch for 10 min",
        "Review financial budget", "Declutter a space", "Do a crossword puzzle"
    ]

    weekly_habits_list = [
        "Clean the kitchen", "Plan the upcoming week", "Call a family member",
        "Try a new recipe", "Go for a long walk", "Do laundry",
        "Meal prep", "Water the plants", "Review goals", "Go grocery shopping",
        "Learn a new song on an instrument", "Go for a bike ride",
        "Write a blog post", "Visit a new coffee shop"
    ]

    habits_to_create = []

    # Create a mix of daily and weekly habits
    for i in range(num_habits):
        if i % 2 == 0:
            name = f"{random.choice(daily_habits_list)} ({i + 1})"
            habits_to_create.append(Habit(name, "daily"))
        else:
            name = f"{random.choice(weekly_habits_list)} ({i + 1})"
            habits_to_create.append(Habit(name, "weekly"))

    # Add each habit to the database
    for habit in habits_to_create:
        habit_id = storage.save_habit(conn, habit)

        # Generate varied completion data for each habit
        completions_to_add = []
        today = datetime.datetime.now()

        if habit.periodicity == "daily":
            # Simulate a continuous streak with occasional missed days over a 3-month period
            for d in range(90):
                if random.random() < 0.85:  # 85% chance of completion
                    completions_to_add.append(today - datetime.timedelta(days=d))
        elif habit.periodicity == "weekly":
            # Simulate a 20-week history
            for w in range(20):
                if random.random() < 0.7:  # 70% chance of completion
                    completions_to_add.append(today - datetime.timedelta(weeks=w))

        for comp_date in completions_to_add:
            storage.save_completion(conn, habit_id, comp_date)

    print(f"Generated and saved a complex dataset of {num_habits} habits.")
    return storage.load_all_habits(conn)


def load_sample_habits(conn, num_daily=25, num_weekly=25, num_weeks=4):
    """
    Creates and saves a simple set of sample habits for basic testing.
    Retained for compatibility with existing tests.
    """
    print("Generating and saving simple sample habits...")
    habits = []

    for i in range(1, num_daily + 1):
        habit = Habit(name=f"Daily Habit {i}", periodicity="daily")
        habit_id = storage.save_habit(conn, habit)
        for d in range(num_weeks * 7):
            completion_date = datetime.datetime.now() - datetime.timedelta(days=d)
            storage.save_completion(conn, habit_id, completion_date)
        habits.append(habit)

    for i in range(1, num_weekly + 1):
        habit = Habit(name=f"Weekly Habit {i}", periodicity="weekly")
        habit_id = storage.save_habit(conn, habit)
        for w in range(num_weeks):
            completion_date = datetime.datetime.now() - datetime.timedelta(weeks=w)
            storage.save_completion(conn, habit_id, completion_date)
        habits.append(habit)

    print(f"Test data for {len(habits)} habits saved successfully.")
    return storage.load_all_habits(conn)