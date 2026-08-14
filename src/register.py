from access import RegisterAccess


class Register32:
    """Represents a 32-bit MCU register."""

    MAX_VALUE = 0xFFFFFFFF
    MIN_BIT = 0
    MAX_BIT = 31

    def __init__(
        self,
        name,
        reset_value=0,
        fields=None,
        access=RegisterAccess.READ_WRITE
    ):
        if not isinstance(access, RegisterAccess):
            raise TypeError(
                "access must be a RegisterAccess value."
            )

        self.name = name
        self.reset_value = reset_value & self.MAX_VALUE
        self.value = self.reset_value
        self.access = access
        self.fields = {}

        if fields:
            for field in fields:
                self.add_field(field)

    def _validate_bit(self, bit):
        if not isinstance(bit, int):
            raise TypeError("Bit number must be an integer.")

        if bit < self.MIN_BIT or bit > self.MAX_BIT:
            raise ValueError(
                "Bit number must be between 0 and 31."
            )

    def _check_read_permission(self):
        if self.access == RegisterAccess.WRITE_ONLY:
            raise PermissionError(
                f"Register '{self.name}' is write-only."
            )

    def _check_write_permission(self):
        if self.access == RegisterAccess.READ_ONLY:
            raise PermissionError(
                f"Register '{self.name}' is read-only."
            )

    def add_field(self, field):
        if field.name in self.fields:
            raise ValueError(
                f"Field '{field.name}' already exists."
            )

        self.fields[field.name] = field

    def read(self):
        self._check_read_permission()
        return self.value

    def write(self, value):
        self._check_write_permission()

        if not isinstance(value, int):
            raise TypeError(
                "Register value must be an integer."
            )

        self.value = value & self.MAX_VALUE

    def reset(self):
        self.value = self.reset_value

    def set_bit(self, bit):
        self._check_write_permission()
        self._validate_bit(bit)
        self.value |= (1 << bit)

    def clear_bit(self, bit):
        self._check_write_permission()
        self._validate_bit(bit)
        self.value &= ~(1 << bit)

    def toggle_bit(self, bit):
        self._check_write_permission()
        self._validate_bit(bit)
        self.value ^= (1 << bit)

    def is_bit_set(self, bit):
        self._check_read_permission()
        self._validate_bit(bit)
        return (self.value & (1 << bit)) != 0

    def read_field(self, field_name):
        self._check_read_permission()

        if field_name not in self.fields:
            raise ValueError(
                f"Unknown field: {field_name}"
            )

        return self.fields[field_name].extract(self.value)

    def write_field(self, field_name, field_value):
        self._check_write_permission()

        if field_name not in self.fields:
            raise ValueError(
                f"Unknown field: {field_name}"
            )

        self.value = self.fields[field_name].insert(
            self.value,
            field_value
        )