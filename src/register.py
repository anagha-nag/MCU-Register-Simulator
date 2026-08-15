from register_field import RegisterField
from access import RegisterAccess

from errors import (
    InvalidRegisterValueError,
    RegisterAccessError
)


class Register32:
    """Simulates a 32-bit MCU register."""

    WIDTH = 32
    MAX_VALUE = 0xFFFFFFFF

    def __init__(
        self,
        name,
        reset_value=0,
        access=RegisterAccess.READ_WRITE
    ):
        if not isinstance(name, str):
            raise TypeError(
                "Register name must be a string."
            )

        if not isinstance(access, RegisterAccess):
            raise TypeError(
                "access must be a RegisterAccess value."
            )

        self.name = name
        self.access = access

        self._validate_value(reset_value)

        self.reset_value = reset_value & self.MAX_VALUE
        self.value = self.reset_value

        self.fields = {}

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_value(self, value):
      """Validate a register value."""

      if not isinstance(value, int):
        raise TypeError(
            "Register value must be an integer."
        )

      if value < 0:
        raise ValueError(
            "Register value cannot be negative."
        )

    def _validate_bit(self, bit):
        if not isinstance(bit, int):
            raise TypeError(
                "Bit position must be an integer."
            )

        if bit < 0 or bit >= self.WIDTH:
            raise ValueError(
                "Bit position must be between 0 and 31."
            )

    # =========================================================
    # READ
    # =========================================================

    def read(self):
        if self.access == RegisterAccess.WRITE_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is write-only."
            )

        return self.value

    # =========================================================
    # WRITE
    # =========================================================

    def write(self, value):
        if self.access == RegisterAccess.READ_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is read-only."
            )

        self._validate_value(value)

        self.value = value & self.MAX_VALUE

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):
        self.value = self.reset_value

    # =========================================================
    # BIT OPERATIONS
    # =========================================================

    def set_bit(self, bit):
        self._validate_bit(bit)

        if self.access == RegisterAccess.READ_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is read-only."
            )

        self.value |= 1 << bit
        self.value &= self.MAX_VALUE

    def clear_bit(self, bit):
        self._validate_bit(bit)

        if self.access == RegisterAccess.READ_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is read-only."
            )

        self.value &= ~(1 << bit)
        self.value &= self.MAX_VALUE

    def toggle_bit(self, bit):
        self._validate_bit(bit)

        if self.access == RegisterAccess.READ_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is read-only."
            )

        self.value ^= 1 << bit
        self.value &= self.MAX_VALUE

    def is_bit_set(self, bit):
        self._validate_bit(bit)

        return bool(
            self.value & (1 << bit)
        )

    # =========================================================
    # FIELDS
    # =========================================================

    def add_field(self, name, lsb, width):
        if not isinstance(name, str):
            raise TypeError(
                "Field name must be a string."
            )

        if name in self.fields:
            raise ValueError(
                f"Field '{name}' already exists."
            )

        field = RegisterField(
            name,
            lsb,
            width
        )

        if (
            field.lsb < 0
            or field.width <= 0
            or field.lsb + field.width > self.WIDTH
        ):
            raise ValueError(
                f"Field '{name}' does not fit "
                f"inside a 32-bit register."
            )

        new_mask = field.mask

        for existing_field in self.fields.values():
            if new_mask & existing_field.mask:
                raise ValueError(
                    f"Field '{name}' overlaps "
                    f"an existing field."
                )

        self.fields[name] = field

    def read_field(self, field_name):
        if self.access == RegisterAccess.WRITE_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is write-only."
            )

        field = self._get_field(field_name)

        return (
            (self.value & field.mask)
            >> field.lsb
        )

    def write_field(self, field_name, field_value):
        if self.access == RegisterAccess.READ_ONLY:
            raise RegisterAccessError(
                f"Register '{self.name}' is read-only."
            )

        field = self._get_field(field_name)

        if not isinstance(field_value, int):
            raise TypeError(
                f"Value for field '{field_name}' "
                f"must be an integer."
            )

        if (
            field_value < 0
            or field_value > field.max_value
        ):
            raise ValueError(
                f"Field '{field_name}' must be "
                f"between 0 and {field.max_value}."
            )

        self.value &= ~field.mask

        self.value |= (
            field_value << field.lsb
        ) & field.mask

        self.value &= self.MAX_VALUE

    def _get_field(self, field_name):
        if field_name not in self.fields:
            raise ValueError(
                f"Unknown field '{field_name}' "
                f"in register '{self.name}'."
            )

        return self.fields[field_name]

    def get_field_names(self):
        return list(self.fields.keys())

    def __repr__(self):
        return (
            f"Register32("
            f"name='{self.name}', "
            f"value=0x{self.value:08X}, "
            f"access={self.access.name}"
            f")"
        )