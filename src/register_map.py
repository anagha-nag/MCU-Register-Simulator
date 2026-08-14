from access import RegisterAccess
from register import Register32
from register_field import RegisterField


class RegisterMap:
    """Simulates the MCU memory-mapped register space."""

    def __init__(self):
        self.registers = {
            0x40000000: Register32(
                "GPIO_CTRL",
                reset_value=0x00000000,
                access=RegisterAccess.READ_WRITE,
                fields=[
                    RegisterField("ENABLE", 0, 1),
                    RegisterField("MODE", 4, 4),
                ]
            ),

            0x40000004: Register32(
                "GPIO_DATA",
                reset_value=0x00000000,
                access=RegisterAccess.READ_WRITE
            ),

            0x40000008: Register32(
                "GPIO_STATUS",
                reset_value=0x00000001,
                access=RegisterAccess.READ_ONLY,
                fields=[
                    RegisterField("READY", 0, 1),
                    RegisterField("ERROR", 1, 1),
                ]
            ),

            0x4000000C: Register32(
                "GPIO_CONFIG",
                reset_value=0x00000010,
                access=RegisterAccess.READ_WRITE
            ),

            0x40000010: Register32(
                "GPIO_COMMAND",
                reset_value=0x00000000,
                access=RegisterAccess.WRITE_ONLY
            ),
        }

    def read(self, address):
        self._validate_address(address)
        return self.registers[address].read()

    def write(self, address, value):
        self._validate_address(address)
        self.registers[address].write(value)

    def reset(self, address):
        self._validate_address(address)
        self.registers[address].reset()

    def set_bit(self, address, bit):
        self._validate_address(address)
        self.registers[address].set_bit(bit)

    def clear_bit(self, address, bit):
        self._validate_address(address)
        self.registers[address].clear_bit(bit)

    def toggle_bit(self, address, bit):
        self._validate_address(address)
        self.registers[address].toggle_bit(bit)

    def get_register_name(self, address):
        self._validate_address(address)
        return self.registers[address].name

    def read_field(self, address, field_name):
        self._validate_address(address)
        return self.registers[address].read_field(field_name)

    def write_field(self, address, field_name, field_value):
        self._validate_address(address)
        self.registers[address].write_field(
            field_name,
            field_value
        )

    def get_access(self, address):
        self._validate_address(address)
        return self.registers[address].access

    def _validate_address(self, address):
        if address not in self.registers:
            raise ValueError(
                f"Invalid register address: 0x{address:08X}"
            )