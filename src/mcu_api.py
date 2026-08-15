from gpio import GPIO


class MCU:
    """High-level public API for the MCU simulator."""

    def __init__(self):
        self.gpio = GPIO()
        self.gpio.configure_output()

    # =====================================================
    # REGISTER API
    # =====================================================

    def read_register(self, address):
        """Read a register by address."""

        return self.gpio.get_register_map().read(
            address
        )

    def write_register(self, address, value):
        """Write a value to a register."""

        self.gpio.get_register_map().write(
            address,
            value
        )

    def reset_register(self, address):
        """Reset a register."""

        self.gpio.get_register_map().reset(
            address
        )

    # =====================================================
    # GPIO API
    # =====================================================

    def enable_gpio(self):
        """Enable the GPIO peripheral."""

        self.gpio.enable()

    def disable_gpio(self):
        """Disable the GPIO peripheral."""

        self.gpio.disable()

    def set_gpio(self, pin):
        """Set a GPIO pin HIGH."""

        self.gpio.set_pin(pin)

    def clear_gpio(self, pin):
        """Set a GPIO pin LOW."""

        self.gpio.clear_pin(pin)

    def toggle_gpio(self, pin):
        """Toggle a GPIO pin."""

        self.gpio.toggle_pin(pin)

    def read_gpio(self, pin):
        """Read a GPIO pin."""

        return self.gpio.read_pin(pin)

    def write_gpio_port(self, value):
        """Write the entire GPIO port."""

        self.gpio.write_port(value)

    def read_gpio_port(self):
        """Read the entire GPIO port."""

        return self.gpio.read_port()

    # =====================================================
    # INTERRUPT API
    # =====================================================

    def enable_gpio_interrupt(self, pin):
        """Enable a GPIO pin interrupt."""

        self.gpio.enable_pin_interrupt(pin)

    def disable_gpio_interrupt(self, pin):
        """Disable a GPIO pin interrupt."""

        self.gpio.disable_pin_interrupt(pin)

    def attach_gpio_interrupt_handler(self, pin, handler):
      """Attach a handler to a GPIO interrupt."""

      self.gpio.attach_pin_interrupt_handler(
        pin,
        handler
    )

    def clear_gpio_interrupt(self, pin):
        """Clear a pending GPIO interrupt."""

        self.gpio.clear_interrupt(pin)

    def service_gpio_interrupt(self, pin):
        """Service a pending GPIO interrupt."""

        return self.gpio.service_interrupt(pin)

    def gpio_interrupt_pending(self, pin):
        """Check whether a GPIO interrupt is pending."""

        return self.gpio.is_interrupt_pending(pin)
    