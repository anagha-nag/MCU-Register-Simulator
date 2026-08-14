class RegisterField:
    """Represents a field inside a 32-bit MCU register."""

    def __init__(self, name, lsb, width):
        self.name = name
        self.lsb = lsb
        self.width = width

        if not isinstance(lsb, int):
            raise TypeError("LSB must be an integer.")

        if not isinstance(width, int):
            raise TypeError("Width must be an integer.")

        if lsb < 0 or lsb > 31:
            raise ValueError("LSB must be between 0 and 31.")

        if width <= 0:
            raise ValueError("Field width must be greater than 0.")

        if lsb + width > 32:
            raise ValueError("Field cannot extend beyond bit 31.")

        self.mask = ((1 << width) - 1) << lsb

    def extract(self, register_value):
        """Extract the field value from a register value."""
        return (register_value & self.mask) >> self.lsb

    def insert(self, register_value, field_value):
        """Insert a field value into a register value."""
        max_value = (1 << self.width) - 1

        if not isinstance(field_value, int):
            raise TypeError("Field value must be an integer.")

        if field_value < 0 or field_value > max_value:
            raise ValueError(
                f"{self.name} must be between 0 and {max_value}."
            )

        register_value &= ~self.mask
        register_value |= (field_value << self.lsb) & self.mask

        return register_value