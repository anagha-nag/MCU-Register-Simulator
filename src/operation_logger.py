from datetime import datetime


class OperationLogger:
    """Stores a history of simulator operations."""

    def __init__(self, max_entries=200):
        self.max_entries = max_entries
        self.history = []

    def log(self, operation, target, value=None):
        timestamp = datetime.now().strftime("%H:%M:%S")

        entry = {
            "time": timestamp,
            "operation": operation,
            "target": target,
            "value": value
        }

        self.history.append(entry)

        if len(self.history) > self.max_entries:
            self.history.pop(0)

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()