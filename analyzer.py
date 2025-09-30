import datetime


def calculate_streak(completions, periodicity):
    """
    Calculates the longest run streak for a given list of completion dates.

    Args:
        completions (list): A list of datetime objects for completions.
        periodicity (str): "daily" or "weekly".

    Returns:
        int: The longest streak count.
    """
    if not completions:
        return 0

    # Sort completions and remove duplicates
    sorted_completions = sorted(list(set(completions)))
    max_streak = 0
    current_streak = 0

    def get_period_start(date, period):
        if period == "daily":
            return date.date()
        elif period == "weekly":
            # For weekly, we find the start of the week (Monday)
            return date.date() - datetime.timedelta(days=date.weekday())
        return None

    for i in range(len(sorted_completions)):
        current_date = sorted_completions[i]

        current_period_start = get_period_start(current_date, periodicity)

        if i == 0:
            current_streak = 1
        else:
            prev_date = sorted_completions[i - 1]
            prev_period_start = get_period_start(prev_date, periodicity)

            # Check if current completion is in the next consecutive period
            if periodicity == "daily":
                expected_prev_day = current_date.date() - datetime.timedelta(days=1)
                if prev_period_start == expected_prev_day:
                    current_streak += 1
                elif prev_period_start != current_period_start:
                    current_streak = 1
            elif periodicity == "weekly":
                expected_prev_week_start = current_period_start - datetime.timedelta(weeks=1)
                if prev_period_start == expected_prev_week_start:
                    current_streak += 1
                elif prev_period_start != current_period_start:
                    current_streak = 1

        if current_streak > max_streak:
            max_streak = current_streak

    return max_streak


def longest_streak(habits):
    """Return the longest streak across all habits."""
    longest = 0
    for h in habits:
        streak = calculate_streak(h.completions, h.periodicity)
        if streak > longest:
            longest = streak
    return longest


def longest_streak_for_habit(habit):
    """Return the longest streak for a given habit."""
    return calculate_streak(habit.completions, habit.periodicity)


def habits_by_periodicity(habits, periodicity):
    """Return all habits matching a periodicity (daily/weekly)."""
    return [h for h in habits if h.periodicity == periodicity]


def top_5_streaks(habits):
    """Return the top 5 habits with longest streaks."""
    # Use the corrected function to get the streak
    return sorted(habits, key=lambda h: longest_streak_for_habit(h), reverse=True)[:5]


def get_last_completion(completions):
    """Returns the timestamp of the last completion."""
    return max(completions) if completions else None


def habits_missed_last_week(habits):
    """Return habits not completed in the last 7 days."""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    # Corrected to use the new get_last_completion helper function
    return [h for h in habits if not get_last_completion(h.completions) or get_last_completion(h.completions) < cutoff]