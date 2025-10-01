import storage
import analyzer
from models import User, Habit
import datetime
import os


# --- Main Application Logic ---
def run_interactive_app(conn):
    """Handles the main application flow after a user is logged in."""
    user_id = None

    while not user_id:
        print("\n--- Welcome! ---")
        print("1. Register")
        print("2. Sign In")
        print("3. Exit")
        print("4. Run Phase 2 Proof Demo (Auto-setup for report)")  # NEW DEMO OPTION
        choice = input("Enter your choice: ")

        if choice == '1':
            full_name = input("Enter your full name: ")
            email = input("Enter your email: ")
            username = input("Choose a username: ")
            password = input("Choose a password: ")

            if storage.register_user(conn, username, password, full_name, email):
                print("Registration successful! Please sign in.")
            else:
                print("Username already exists. Please try a different one.")
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = storage.login_user(conn, username, password)
            if user_id:
                print("Sign in successful!")
            else:
                print("Invalid username or password.")
        elif choice == '3':
            return
        elif choice == '4':
            # Run the test data setup and log in automatically
            try:
                # Note: storage.add_test_data must be defined in storage.py
                user_id, username, password = storage.add_test_data(conn)
                if user_id:
                    print(f"Logged in as proof user: {username}")
                    generate_proof_screenshots(conn, user_id)
                else:
                    print("Proof demo setup failed.")
            except Exception as e:
                print(f"An error occurred during proof setup: {e}")

            if user_id:
                # After running the proof, go straight to the main menu
                break
            else:
                continue  # Go back to welcome menu
        else:
            print("Invalid choice. Please try again.")

    # Main menu loop after successful sign-in
    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new habit")
        print("2. Log a habit completion")
        print("3. View analytics")
        print("4. Delete a habit")
        print("5. Delete my account")
        print("6. Sign out")
        print("7. View Raw Data (for persistence proof)")  # NEW DATA OPTION

        choice = input("Enter your choice: ")

        if choice == '1':
            create_habit_cli(conn, user_id)
        elif choice == '2':
            log_completion_cli(conn, user_id)
        elif choice == '3':
            analyze_habits_cli(conn, user_id)
        elif choice == '4':
            delete_habit_cli(conn, user_id)
        elif choice == '5':
            confirm = input("Are you sure you want to delete your account? This cannot be undone. (yes/no): ")
            if confirm.lower() == 'yes':
                storage.delete_user(conn, user_id)
                print("Account deleted. Goodbye!")
                return
        elif choice == '6':
            print("Signing out...")
            return
        elif choice == '7':
            view_raw_data_cli(conn, user_id)
        else:
            print("Invalid choice. Please try again.")


# --- CLI Helper Functions ---
def create_habit_cli(conn, user_id):
    """Handles the user input for creating a new habit."""
    name = input("Enter habit name: ")
    periodicity = input("Enter periodicity (daily, weekly): ").lower()
    if periodicity not in ['daily', 'weekly']:
        print("Invalid periodicity. Please choose 'daily' or 'weekly'.")
        return
    h = Habit(name, periodicity)
    storage.save_habit(conn, user_id, h)
    print(f"Habit '{name}' created successfully!")


def log_completion_cli(conn, user_id):
    """Handles logging a completion for a chosen habit."""
    habits = storage.load_habits_for_user(conn, user_id)
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


def delete_habit_cli(conn, user_id):
    """Handles deleting a chosen habit."""
    habits = storage.load_habits_for_user(conn, user_id)
    if not habits:
        print("No habits found to delete.")
        return

    print("\nSelect a habit to delete:")
    for i, h in enumerate(habits):
        print(f"{i + 1}. {h.name} ({h.periodicity})")

    try:
        choice = int(input("Enter habit number to delete: "))
        if 1 <= choice <= len(habits):
            habit_id = habits[choice - 1].habit_id
            storage.delete_habit(conn, habit_id)
            print(f"Habit '{habits[choice - 1].name}' successfully deleted.")
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def analyze_habits_cli(conn, user_id):
    """Presents the analysis menu and handles user choices."""
    habits = storage.load_habits_for_user(conn, user_id)
    if not habits:
        print("No habits found to analyze.")
        return

    while True:
        print("\n--- Analytics Menu ---")
        print("1. List all tracked habits")
        print("2. Filter habits by periodicity")
        print("3. View global longest streak")
        print("4. View longest streak for a specific habit")
        print("5. Return to main menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nAll Tracked Habits:")
            for h in habits:
                print(f"- {h.name} ({h.periodicity})")

        elif choice == '2':
            period = input("Filter by 'daily' or 'weekly': ").lower()
            filtered = analyzer.filter_habits_by_periodicity(habits, period)
            print(f"\n{period.capitalize()} Habits:")
            for h in filtered:
                print(f"- {h.name}")

        elif choice == '3':
            longest = analyzer.longest_streak(habits)
            print(f"\nOverall Longest Streak Across All Habits: {longest}")

        elif choice == '4':
            print("\nSelect habit to analyze:")
            for i, h in enumerate(habits):
                print(f"{i + 1}. {h.name}")

            try:
                habit_choice = int(input("Enter habit number: "))
                if 1 <= habit_choice <= len(habits):
                    habit = habits[habit_choice - 1]
                    streak = analyzer.calculate_streak(habit.completions, habit.periodicity)
                    print(f"\nLongest Streak for '{habit.name}': {streak}")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")

        elif choice == '5':
            return

        else:
            print("Invalid choice. Please try again.")


def view_raw_data_cli(conn, user_id):
    """Displays raw data and timestamps for persistence proof."""
    habits = storage.load_habits_for_user(conn, user_id)
    if not habits:
        print("No habits found.")
        return

    print("\n--- RAW DATA LOGS (For Phase 2 Proof) ---")
    for i, h in enumerate(habits):
        print(f"\n[{i + 1}. {h.name} ({h.periodicity})]")
        print(f"  Habit ID: {h.habit_id}")
        # The 'created_at' attribute is a datetime object or iso string from the Habit model
        print(f"  Created At: {h.created_at}")

        print(f"  Completions ({len(h.completions)} logs):")
        for log in h.completions:
            print(
                f"    - {log.isoformat() if isinstance(log, datetime.datetime) else log}")  # Ensure datetime is formatted
    print("------------------------------------------")


def generate_proof_screenshots(conn, user_id):
    """Generates the required streak outputs for the lecturer."""
    habits = storage.load_habits_for_user(conn, user_id)

    # 1. RAW DATA PROOF (Timestamps + 5+ habits + 4 weeks)
    view_raw_data_cli(conn, user_id)
    print("\n*** SCREENSHOT 1: Capture the RAW DATA above (Habit names and ALL log timestamps) ***")

    # 2. STREAK PROOF (Daily vs Weekly logic)
    # Check if the expected test habits exist before proceeding
    try:
        daily_habit = next(h for h in habits if h.name == "Daily Reading")
        weekly_habit = next(h for h in habits if h.name == "Weekly Budget Review")
    except StopIteration:
        print("\nERROR: Test habits not found. Did you run option 4 first?")
        return

    print("\n--- STREAK PROOF ---")

    # Daily Proof (Expected streak: 5)
    daily_streak = analyzer.calculate_streak(daily_habit.completions, daily_habit.periodicity)
    print(f"[{daily_habit.name}]: Periodicity={daily_habit.periodicity}. Longest Streak: {daily_streak}")

    # Weekly Proof (Expected streak: 4)
    weekly_streak = analyzer.calculate_streak(weekly_habit.completions, weekly_habit.periodicity)
    print(f"[{weekly_habit.name}]: Periodicity={weekly_habit.periodicity}. Longest Streak: {weekly_streak}")

    # Overall Longest Streak Proof
    overall_longest = analyzer.longest_streak(habits)
    print(f"Overall Longest Streak Across All Habits: {overall_longest}")

    print("\n*** SCREENSHOT 2: Capture the STREAK PROOF above (Daily=5, Weekly=4, Overall=5) ***")
    print("\n------------------------------------------------------------------------------------")
    print("DEMO COMPLETE. You are now logged into the proof user account.")


# --- Main function to run the application ---
if __name__ == "__main__":
    conn = storage.get_db_connection()
    storage.create_tables(conn)
    run_interactive_app(conn)
    conn.close()
