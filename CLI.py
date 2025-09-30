# CLI.py
import storage
import analyzer
import datetime
from habit import Habit


def display_main_menu():
    """Displays the main menu options to the user."""
    print("\n--- Main Menu ---")
    print("1. Create a new habit")
    print("2. Log a completion")
    print("3. Analyze my habits")
    print("4. Exit")


def get_user_choice():
    """Gets the user's choice from the menu."""
    return input("Enter your choice: ")


def create_habit_cli(conn):
    """Handles the user input for creating a new habit."""
    name = input("Enter habit name: ")
    periodicity = input("Enter periodicity (daily or weekly): ").lower()
    if periodicity not in ['daily', 'weekly']:
        print("Invalid periodicity. Please choose 'daily' or 'weekly'.")
        return
    h = Habit(name, periodicity)
    storage.save_habit(conn, h)
    print(f"Habit '{name}' created successfully!")


def log_completion_cli(conn):
    """Handles logging a completion for a chosen habit."""
    habits = storage.load_all_habits(conn)
    if not habits:
        print("No habits found. Please create one first.")
        return

    print("\nSelect a habit to log completion for:")
    for i, h in enumerate(habits):
        print(f"{i + 1}. {h.name} ({h.periodicity})")

    try:
        choice = int(input("Enter habit number: "))
        if 1 <= choice <= len(habits):
            habit = habits[choice - 1]
            storage.save_completion(conn, habit.habit_id, datetime.datetime.now())
            print(f"Completion logged for '{habit.name}'.")
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def analyze_habits_cli(conn):
    """Presents the analysis menu and handles user choices."""
    habits = storage.load_all_habits(conn)
    if not habits:
        print("No habits found to analyze.")
        return

    print("\n--- Analysis Menu ---")
    print("1. View all habits")
    print("2. Filter habits by periodicity")
    print("3. Show the longest streak for a specific habit")
    print("4. Show the overall longest streak")
    print("5. Show habits missed in the last week")
    analysis_choice = input("Enter your choice: ")

    if analysis_choice == '1':
        print("\nAll Tracked Habits:")
        for habit in habits:
            print(f"- {habit.name} ({habit.periodicity})")

    elif analysis_choice == '2':
        period = input("Enter periodicity (daily or weekly): ").lower()
        filtered_habits = analyzer.habits_by_periodicity(habits, period)
        if filtered_habits:
            print(f"\n{period.capitalize()} Habits:")
            for habit in filtered_habits:
                print(f"- {habit.name}")
        else:
            print(f"No {period} habits found.")

    elif analysis_choice == '3':
        print("\nSelect a habit to view its streak:")
        for i, h in enumerate(habits):
            print(f"{i + 1}. {h.name}")

        try:
            choice = int(input("Enter habit number: "))
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                streak = analyzer.calculate_streak(habit.completions, habit.periodicity)
                print(f"Longest streak for '{habit.name}' is: {streak}")
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    elif analysis_choice == '4':
        longest = analyzer.longest_streak(habits)
        print(f"\nOverall longest streak is: {longest}")

    elif analysis_choice == '5':
        missed = analyzer.habits_missed_last_week(habits)
        if missed:
            print("\nHabits Missed in the Last Week:")
            for habit in missed:
                print(f"- {habit.name}")
        else:
            print("No habits were missed last week. Great job!")