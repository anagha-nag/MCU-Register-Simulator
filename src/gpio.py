from register_map import RegisterMap
from interrupt_controller import InterruptController
from event_manager import EventManager

from errors import (
    GPIOConfigurationError,
    GPIOPinError
)


class GPIO:
    """Simulated 8-pin GPIO peripheral."""

    # =========================================================
    # REGISTER ADDRESSES
    # =========================================================

    GPIO_CTRL = 0x40000000
    GPIO_DATA = 0x40000004
    GPIO_STATUS = 0x40000008

    # =========================================================
    # REGISTER FIELDS
    # =========================================================

    ENABLE_FIELD = "ENABLE"
    MODE_FIELD = "MODE"

    READY_FIELD = "READY"
    ERROR_FIELD = "ERROR"

    # =========================================================
    # GPIO MODES
    # =========================================================

    INPUT_MODE = 0
    OUTPUT_MODE = 1

    # =========================================================
    # CONFIGURATION
    # =========================================================

    NUM_PINS = 8

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):
        """Initialize the GPIO peripheral."""

        self.registers = RegisterMap()

        # Simulated pin states.
        self.pins = [0] * self.NUM_PINS

        # Interrupt controller.
        self.interrupts = InterruptController()

        # General event system.
        self.events = EventManager()

        # Create one interrupt source per GPIO pin.
        self._configure_interrupts()

        # Initial status.
        self._set_ready(True)
        self._set_error(False)

    # =========================================================
    # INTERRUPT CONFIGURATION
    # =========================================================

    def _configure_interrupts(self):
        """Create GPIO0_CHANGE ... GPIO7_CHANGE."""

        for pin in range(self.NUM_PINS):
            interrupt_name = f"GPIO{pin}_CHANGE"

            self.interrupts.register_interrupt(
                interrupt_name
            )

    def enable_pin_interrupt(self, pin):
        """Enable a GPIO pin-change interrupt."""

        self._validate_pin(pin)

        self.interrupts.enable_interrupt(
            f"GPIO{pin}_CHANGE"
        )

    def disable_pin_interrupt(self, pin):
        """Disable a GPIO pin-change interrupt."""

        self._validate_pin(pin)

        self.interrupts.disable_interrupt(
            f"GPIO{pin}_CHANGE"
        )

    def attach_pin_interrupt_handler(
        self,
        pin,
        handler
    ):
        """Attach an ISR/callback to a GPIO pin."""

        self._validate_pin(pin)

        self.interrupts.attach_handler(
            f"GPIO{pin}_CHANGE",
            handler
        )

    # =========================================================
    # INTERRUPT CONTROL
    # =========================================================

    def service_interrupt(self, pin):
        """Service a pending GPIO interrupt."""

        self._validate_pin(pin)

        return self.interrupts.service_interrupt(
            f"GPIO{pin}_CHANGE"
        )

    def clear_interrupt(self, pin):
        """Clear a pending GPIO interrupt."""

        self._validate_pin(pin)

        self.interrupts.clear_pending(
            f"GPIO{pin}_CHANGE"
        )

    def is_interrupt_pending(self, pin):
        """Return True if the GPIO interrupt is pending."""

        self._validate_pin(pin)

        return self.interrupts.is_pending(
            f"GPIO{pin}_CHANGE"
        )

    def is_interrupt_enabled(self, pin):
        """Return True if the GPIO interrupt is enabled."""

        self._validate_pin(pin)

        return self.interrupts.is_enabled(
            f"GPIO{pin}_CHANGE"
        )

    def get_interrupt_count(self, pin):
        """Return the number of times the interrupt was raised."""

        self._validate_pin(pin)

        return self.interrupts.get_trigger_count(
            f"GPIO{pin}_CHANGE"
        )

    # =========================================================
    # EVENT SYSTEM
    # =========================================================

    def subscribe_event(
        self,
        event_name,
        callback
    ):
        """Subscribe to a GPIO event."""

        self.events.subscribe(
            event_name,
            callback
        )

    def _notify_pin_change(self, pin):
        """
        Publish a GPIO change event and raise its interrupt.
        """

        event_data = {
            "pin": pin,
            "state": self.pins[pin]
        }

        # General GPIO event.
        self.events.publish(
            "GPIO_CHANGE",
            event_data
        )

        # Raise interrupt.
        # The interrupt remains pending until serviced.
        self.interrupts.raise_interrupt(
            f"GPIO{pin}_CHANGE",
            event_data
        )

    def _notify_register_write(
        self,
        address,
        value
    ):
        """Publish a register-write event."""

        event_data = {
            "address": address,
            "value": value
        }

        self.events.publish(
            "REGISTER_WRITE",
            event_data
        )

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_pin(self, pin):
     """Validate a GPIO pin number."""

     if not isinstance(pin, int):
        raise TypeError(
            "Pin number must be an integer."
        )

     if pin < 0 or pin >= self.NUM_PINS:
        raise GPIOPinError(
            f"Pin number must be between "
            f"0 and {self.NUM_PINS - 1}."
        )

    # =========================================================
    # INTERNAL STATE
    # =========================================================

    def _is_enabled(self):
        """Return True if GPIO is enabled."""

        return (
            self.registers.read_field(
                self.GPIO_CTRL,
                self.ENABLE_FIELD
            ) == 1
        )

    def _is_output_mode(self):
        """Return True if GPIO is in output mode."""

        return (
            self.registers.read_field(
                self.GPIO_CTRL,
                self.MODE_FIELD
            ) == self.OUTPUT_MODE
        )

    # =========================================================
    # STATUS
    # =========================================================

    def _set_ready(self, state):
        """Update the READY status bit."""

        status_register = (
            self.registers.registers[
                self.GPIO_STATUS
            ]
        )

        if state:
            status_register.value |= 0x00000001
        else:
            status_register.value &= ~0x00000001

    def _set_error(self, state):
        """Update the ERROR status bit."""

        status_register = (
            self.registers.registers[
                self.GPIO_STATUS
            ]
        )

        if state:
            status_register.value |= 0x00000002
        else:
            status_register.value &= ~0x00000002

    def _set_error_and_raise(self, message):
        """Set the error flag and raise a GPIO error."""

        self._set_error(True)

        raise GPIOConfigurationError(message)

    # =========================================================
    # REGISTER SIDE EFFECTS
    # =========================================================

    def _apply_register_side_effects(self):
        """Apply hardware-like effects of GPIO_CTRL."""

        enabled = self._is_enabled()

        # READY follows ENABLE.
        self._set_ready(enabled)

        # Disable clears the error flag.
        if not enabled:
            self._set_error(False)

    # =========================================================
    # ENABLE / DISABLE
    # =========================================================

    def enable(self):
        """Enable the GPIO peripheral."""

        self.registers.write_field(
            self.GPIO_CTRL,
            self.ENABLE_FIELD,
            1
        )

        self._apply_register_side_effects()
        self._set_error(False)

        self._notify_register_write(
            self.GPIO_CTRL,
            self.registers.read(
                self.GPIO_CTRL
            )
        )

    def disable(self):
        """Disable the GPIO peripheral."""

        self.registers.write_field(
            self.GPIO_CTRL,
            self.ENABLE_FIELD,
            0
        )

        self._apply_register_side_effects()

        self._notify_register_write(
            self.GPIO_CTRL,
            self.registers.read(
                self.GPIO_CTRL
            )
        )

    # =========================================================
    # MODE CONTROL
    # =========================================================

    def set_mode(self, mode):
        """Set GPIO operating mode."""

        if mode not in (
            self.INPUT_MODE,
            self.OUTPUT_MODE
        ):
            raise GPIOConfigurationError(
                "Mode must be INPUT_MODE (0) "
                "or OUTPUT_MODE (1)."
            )

        self.registers.write_field(
            self.GPIO_CTRL,
            self.MODE_FIELD,
            mode
        )

        self._notify_register_write(
            self.GPIO_CTRL,
            self.registers.read(
                self.GPIO_CTRL
            )
        )

    def configure_output(self):
        """Enable GPIO and configure output mode."""

        self.enable()

        self.set_mode(
            self.OUTPUT_MODE
        )

    def configure_input(self):
        """Enable GPIO and configure input mode."""

        self.enable()

        self.set_mode(
            self.INPUT_MODE
        )

    # =========================================================
    # SET PIN
    # =========================================================

    def set_pin(self, pin):
        """Set a GPIO pin HIGH."""

        self._validate_pin(pin)

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        if not self._is_output_mode():
            self._set_error_and_raise(
                "GPIO is not configured for output mode."
            )

        # No state change -> no interrupt.
        if self.pins[pin] == 1:
            self._set_error(False)
            return

        self.pins[pin] = 1

        self.registers.set_bit(
            self.GPIO_DATA,
            pin
        )

        self._set_error(False)

        self._notify_pin_change(
            pin
        )

        self._notify_register_write(
            self.GPIO_DATA,
            self.registers.read(
                self.GPIO_DATA
            )
        )

    # =========================================================
    # CLEAR PIN
    # =========================================================

    def clear_pin(self, pin):
        """Set a GPIO pin LOW."""

        self._validate_pin(pin)

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        if not self._is_output_mode():
            self._set_error_and_raise(
                "GPIO is not configured for output mode."
            )

        # No state change -> no interrupt.
        if self.pins[pin] == 0:
            self._set_error(False)
            return

        self.pins[pin] = 0

        self.registers.clear_bit(
            self.GPIO_DATA,
            pin
        )

        self._set_error(False)

        self._notify_pin_change(
            pin
        )

        self._notify_register_write(
            self.GPIO_DATA,
            self.registers.read(
                self.GPIO_DATA
            )
        )

    # =========================================================
    # TOGGLE PIN
    # =========================================================

    def toggle_pin(self, pin):
        """Toggle a GPIO pin."""

        self._validate_pin(pin)

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        if not self._is_output_mode():
            self._set_error_and_raise(
                "GPIO is not configured for output mode."
            )

        self.pins[pin] ^= 1

        self.registers.toggle_bit(
            self.GPIO_DATA,
            pin
        )

        self._set_error(False)

        self._notify_pin_change(
            pin
        )

        self._notify_register_write(
            self.GPIO_DATA,
            self.registers.read(
                self.GPIO_DATA
            )
        )

    # =========================================================
    # READ PIN
    # =========================================================

    def read_pin(self, pin):
        """Read the current GPIO pin state."""

        self._validate_pin(pin)

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        self._set_error(False)

        return self.pins[pin]

    # =========================================================
    # WRITE PORT
    # =========================================================

    def write_port(self, value):
        """Write all eight GPIO pins at once."""

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        if not self._is_output_mode():
            self._set_error_and_raise(
                "GPIO is not configured for output mode."
            )

        if not isinstance(value, int):
            raise TypeError(
                "GPIO port value must be an integer."
            )

        if value < 0 or value > 0xFF:
            raise ValueError(
                "GPIO port value must be between "
                "0x00 and 0xFF."
            )

        # Remember old states.
        previous_pins = list(
            self.pins
        )

        # Update GPIO_DATA.
        self.registers.write(
            self.GPIO_DATA,
            value
        )

        # Update simulated pins.
        for pin in range(self.NUM_PINS):
            self.pins[pin] = (
                value >> pin
            ) & 1

        self._set_error(False)

        # Notify register write.
        self._notify_register_write(
            self.GPIO_DATA,
            value
        )

        # Notify only changed pins.
        for pin in range(self.NUM_PINS):

            if (
                self.pins[pin]
                != previous_pins[pin]
            ):
                self._notify_pin_change(
                    pin
                )

    # =========================================================
    # READ PORT
    # =========================================================

    def read_port(self):
        """Read the current GPIO port value."""

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        self._set_error(False)

        return self.registers.read(
            self.GPIO_DATA
        )

    # =========================================================
    # STATUS API
    # =========================================================

    def is_ready(self):
        """Return whether the GPIO is ready."""

        return (
            self.registers.read_field(
                self.GPIO_STATUS,
                self.READY_FIELD
            ) == 1
        )

    def has_error(self):
        """Return whether the GPIO has an error."""

        return (
            self.registers.read_field(
                self.GPIO_STATUS,
                self.ERROR_FIELD
            ) == 1
        )

    def clear_error(self):
        """Clear the GPIO error flag."""

        self._set_error(False)

    # =========================================================
    # REGISTER MAP ACCESS
    # =========================================================

    def get_register_map(self):
        """Return the underlying RegisterMap."""

        return self.registers