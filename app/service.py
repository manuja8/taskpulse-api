LOW_PRIORITY_LIMIT = 2


def classify_task_priority(open_dependencies: int) -> str:
    """Return a simple priority label for a task."""
    if open_dependencies > LOW_PRIORITY_LIMIT:
        return "HIGH"
    return "NORMAL"


def completion_percentage(done: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((done / total) * 100, 2)
