def calculate_rate(damper: float, volume_per_sec: float) -> float:
    rate = volume_per_sec / (60 * 60)  # minutes * hour
    try:
        return rate / (damper / 100)  # convert to percent
    except ZeroDivisionError:
        return 0


def reverse_rate(damper: float, goal_ach: float):
    rate = goal_ach * (damper / 100)
    return rate * 60 * 60

