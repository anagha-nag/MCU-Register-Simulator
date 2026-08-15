class EventManager:
    """Simple publish/subscribe event system."""

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, callback):
        """Subscribe a callback to an event."""

        if not callable(callback):
            raise TypeError(
                "Event callback must be callable."
            )

        self.subscribers.setdefault(
            event_name,
            []
        ).append(callback)

    def unsubscribe(self, event_name, callback):
        """Remove a callback from an event."""

        if event_name not in self.subscribers:
            return

        if callback in self.subscribers[event_name]:
            self.subscribers[event_name].remove(
                callback
            )

    def publish(self, event_name, data=None):
        """Publish an event."""

        for callback in self.subscribers.get(
            event_name,
            []
        ):
            callback(data)