from errors import InvalidFieldValueError


class RegisterField:
    """Represents a named bit field inside a 32-bit register."""

    MAX_WIDTH = 32

    def __init__(
        self,
        name,
        lsb,
        width
    ):
        if not isinstance(name, str):
            raise TypeError(
                "Field name must be a string."
            )

        if not isinstance(lsb, int):
            raise TypeError(
                "LSB must be an integer."
            )

        if not isinstance(width, int):
            raise TypeError(
                "Field width must be an integer."
            )

        if lsb < 0:
            raise ValueError(
                "LSB cannot be negative."
            )

        if width <= 0:
            raise ValueError(
                "Field width must be greater than zero."
            )

        if width > self.MAX_WIDTH:
            raise ValueError(
                "Field width cannot exceed 32 bits."
            )

        if lsb + width > 32:
            raise ValueError(
                "Field cannot extend beyond bit 31."
            )

        self.name = name
        self.lsb = lsb
        self.width = width

    @property
    def mask(self):
        """Return the field bit mask."""

        return (
            ((1 << self.width) - 1)
            << self.lsb
        )

    @property
    def max_value(self):
        """Return the maximum value for this field."""

        return (
            (1 << self.width) - 1
        )

    def validate_value(self, value):
        """Validate a value for this field."""

        if not isinstance(value, int):
            raise TypeError(
                f"Value for field '{self.name}' "
                f"must be an integer."
            )

        if value < 0 or value > self.max_value:
            raise InvalidFieldValueError(
                f"Field '{self.name}' must be "
                f"between 0 and {self.max_value}."
            )

    def extract(self, register_value):
        """Extract this field from a register value."""

        return (
            register_value & self.mask
        ) >> self.lsb

    def insert(
        self,
        register_value,
        field_value
    ):
        """Insert a field value into a register value."""

        self.validate_value(field_value)

        register_value &= ~self.mask

        register_value |= (
            field_value << self.lsb
        ) & self.mask

        return register_value

    def __repr__(self):
        return (
            f"RegisterField("
            f"name='{self.name}', "
            f"lsb={self.lsb}, "
            f"width={self.width}"
            f")"
        )