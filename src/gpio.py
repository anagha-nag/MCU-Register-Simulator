from register_map import RegisterMap


class GPIO:
    """Simulates an 8-pin GPIO peripheral."""

    GPIO_CTRL = 0x40000000
    GPIO_DATA = 0x40000004
    GPIO_STATUS = 0x40000008

    ENABLE_FIELD = "ENABLE"
    MODE_FIELD = "MODE"

    READY_FIELD = "READY"
    ERROR_FIELD = "ERROR"

    INPUT_MODE = 0
    OUTPUT_MODE = 1

    NUM_PINS = 8

    def __init__(self):
        self.registers = RegisterMap()

        # Internal representation of the GPIO pins.
        self.pins = [0] * self.NUM_PINS

        # GPIO is ready when created.
        self._set_ready(True)
        self._set_error(False)

    # --------------------------------------------------
    # Internal validation
    # --------------------------------------------------

    def _validate_pin(self, pin):
        if not isinstance(pin, int):
            raise TypeError("Pin number must be an integer.")

        if pin < 0 or pin >= self.NUM_PINS:
            raise ValueError(
                f"Pin number must be between 0 and {self.NUM_PINS - 1}."
            )

    def _is_enabled(self):
        return (
            self.registers.read_field(
                self.GPIO_CTRL,
                self.ENABLE_FIELD
            ) == 1
        )

    def _is_output_mode(self):
        return (
            self.registers.read_field(
                self.GPIO_CTRL,
                self.MODE_FIELD
            ) == self.OUTPUT_MODE
        )

    # --------------------------------------------------
    # Internal status control
    # --------------------------------------------------

    def _set_ready(self, state):
        status_register = self.registers.registers[self.GPIO_STATUS]

        if state:
            status_register.value |= 1
        else:
            status_register.value &= ~1

    def _set_error(self, state):
        status_register = self.registers.registers[self.GPIO_STATUS]

        if state:
            status_register.value |= (1 << 1)
        else:
            status_register.value &= ~(1 << 1)

    def _set_error_and_raise(self, message):
        self._set_error(True)
        raise RuntimeError(message)

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def enable(self):
        """Enable the GPIO peripheral."""
        self.registers.write_field(
            self.GPIO_CTRL,
            self.ENABLE_FIELD,
            1
        )
        self._set_error(False)

    def disable(self):
        """Disable the GPIO peripheral."""
        self.registers.write_field(
            self.GPIO_CTRL,
            self.ENABLE_FIELD,
            0
        )

    def set_mode(self, mode):
        """Set GPIO mode."""
        if mode not in (self.INPUT_MODE, self.OUTPUT_MODE):
            raise ValueError(
                "Mode must be INPUT_MODE (0) or OUTPUT_MODE (1)."
            )

        self.registers.write_field(
            self.GPIO_CTRL,
            self.MODE_FIELD,
            mode
        )

    def configure_output(self):
        """Enable GPIO and configure it for output."""
        self.enable()
        self.set_mode(self.OUTPUT_MODE)

    def configure_input(self):
        """Enable GPIO and configure it for input."""
        self.enable()
        self.set_mode(self.INPUT_MODE)

    # --------------------------------------------------
    # Pin operations
    # --------------------------------------------------

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

        self.pins[pin] = 1

        self.registers.set_bit(
            self.GPIO_DATA,
            pin
        )

        self._set_error(False)

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

        self.pins[pin] = 0

        self.registers.clear_bit(
            self.GPIO_DATA,
            pin
        )

        self._set_error(False)

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

    def read_pin(self, pin):
        """Read the current state of a GPIO pin."""
        self._validate_pin(pin)

        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        self._set_error(False)

        return self.pins[pin]

    # --------------------------------------------------
    # Port operations
    # --------------------------------------------------

    def write_port(self, value):
        """Write all 8 GPIO pins at once."""
        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        if not self._is_output_mode():
            self._set_error_and_raise(
                "GPIO is not configured for output mode."
            )

        if not isinstance(value, int):
            raise TypeError("GPIO port value must be an integer.")

        if value < 0 or value > 0xFF:
            raise ValueError(
                "GPIO port value must be between 0x00 and 0xFF."
            )

        self.registers.write(
            self.GPIO_DATA,
            value
        )

        for pin in range(self.NUM_PINS):
            self.pins[pin] = (value >> pin) & 1

        self._set_error(False)

    def read_port(self):
        """Read the current 8-bit GPIO port value."""
        if not self._is_enabled():
            self._set_error_and_raise(
                "GPIO peripheral is disabled."
            )

        return self.registers.read(self.GPIO_DATA)

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_ready(self):
        return self.registers.read_field(
            self.GPIO_STATUS,
            self.READY_FIELD
        ) == 1

    def has_error(self):
        return self.registers.read_field(
            self.GPIO_STATUS,
            self.ERROR_FIELD
        ) == 1

    def clear_error(self):
        self._set_error(False)

    def get_register_map(self):
        """Return the underlying register map."""
        return self.registers