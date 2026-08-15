from errors import (
    InterruptNotFoundError,
    InterruptConfigurationError
)


class InterruptController:
    """Simulates an MCU interrupt controller."""

    def __init__(self):
        self.handlers = {}
        self.enabled = {}
        self.pending = {}
        self.pending_data = {}
        self.trigger_count = {}

    # =========================================================
    # REGISTRATION
    # =========================================================

    def register_interrupt(self, interrupt_name):
        if interrupt_name in self.handlers:
            raise ValueError(
                f"Interrupt '{interrupt_name}' already exists."
            )

        self.handlers[interrupt_name] = None
        self.enabled[interrupt_name] = False
        self.pending[interrupt_name] = False
        self.pending_data[interrupt_name] = None
        self.trigger_count[interrupt_name] = 0

    # =========================================================
    # HANDLER
    # =========================================================

    def attach_handler(
        self,
        interrupt_name,
        handler
    ):
        self._validate_interrupt(
            interrupt_name
        )

        if not callable(handler):
            raise InterruptConfigurationError(
                "Interrupt handler must be callable."
            )

        self.handlers[interrupt_name] = handler

    # =========================================================
    # ENABLE / DISABLE
    # =========================================================

    def enable_interrupt(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        self.enabled[interrupt_name] = True

    def disable_interrupt(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        self.enabled[interrupt_name] = False

    # =========================================================
    # RAISE
    # =========================================================

    def raise_interrupt(
        self,
        interrupt_name,
        event_data=None
    ):
        self._validate_interrupt(
            interrupt_name
        )

        self.pending[interrupt_name] = True

        self.pending_data[interrupt_name] = (
            event_data
        )

        self.trigger_count[
            interrupt_name
        ] += 1

    # =========================================================
    # SERVICE
    # =========================================================

    def service_interrupt(
        self,
        interrupt_name,
        event_data=None
    ):
        self._validate_interrupt(
            interrupt_name
        )

        if not self.pending[interrupt_name]:
            return False

        if not self.enabled[interrupt_name]:
            return False

        handler = self.handlers[
            interrupt_name
        ]

        if handler is None:
            return False

        if event_data is None:
            event_data = self.pending_data[
                interrupt_name
            ]

        handler(event_data)

        self.pending[
            interrupt_name
        ] = False

        self.pending_data[
            interrupt_name
        ] = None

        return True

    # =========================================================
    # BACKWARD-COMPATIBLE TRIGGER
    # =========================================================

    def trigger_interrupt(
        self,
        interrupt_name,
        event_data=None
    ):
        self.raise_interrupt(
            interrupt_name,
            event_data
        )

        return self.service_interrupt(
            interrupt_name,
            event_data
        )

    # =========================================================
    # PENDING
    # =========================================================

    def clear_pending(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        self.pending[
            interrupt_name
        ] = False

        self.pending_data[
            interrupt_name
        ] = None

    def is_pending(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        return self.pending[
            interrupt_name
        ]

    # =========================================================
    # STATUS
    # =========================================================

    def is_enabled(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        return self.enabled[
            interrupt_name
        ]

    def get_trigger_count(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        return self.trigger_count[
            interrupt_name
        ]

    def get_status(self, interrupt_name):
        self._validate_interrupt(
            interrupt_name
        )

        return {
            "enabled": self.enabled[interrupt_name],
            "pending": self.pending[interrupt_name],
            "trigger_count": self.trigger_count[
                interrupt_name
            ]
        }

    def get_all_status(self):
        return {
            name: {
                "enabled": self.enabled[name],
                "pending": self.pending[name],
                "trigger_count": self.trigger_count[name]
            }
            for name in self.handlers
        }

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_interrupt(self, interrupt_name):
        if interrupt_name not in self.handlers:
            raise InterruptNotFoundError(
                f"Unknown interrupt: "
                f"{interrupt_name}"
            )