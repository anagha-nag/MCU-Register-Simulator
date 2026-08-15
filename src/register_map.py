from register import Register32
from access import RegisterAccess

from errors import RegisterNotFoundError


class RegisterMap:
    """Maps MCU register addresses to Register32 objects."""

    def __init__(self):
        self.registers = {}

        self._create_default_registers()

    # =========================================================
    # DEFAULT REGISTERS
    # =========================================================

    def _create_default_registers(self):
        gpio_ctrl = Register32(
            "GPIO_CTRL",
            reset_value=0x00000000,
            access=RegisterAccess.READ_WRITE
        )

        gpio_ctrl.add_field(
            "ENABLE",
            0,
            1
        )

        gpio_ctrl.add_field(
            "MODE",
            4,
            4
        )

        gpio_data = Register32(
            "GPIO_DATA",
            reset_value=0x00000000,
            access=RegisterAccess.READ_WRITE
        )

        gpio_status = Register32(
            "GPIO_STATUS",
            reset_value=0x00000001,
            access=RegisterAccess.READ_ONLY
        )

        gpio_status.add_field(
            "READY",
            0,
            1
        )

        gpio_status.add_field(
            "ERROR",
            1,
            1
        )

        gpio_config = Register32(
            "GPIO_CONFIG",
            reset_value=0x00000010,
            access=RegisterAccess.READ_WRITE
        )

        gpio_command = Register32(
            "GPIO_COMMAND",
            reset_value=0x00000000,
            access=RegisterAccess.WRITE_ONLY
        )

        self.registers = {
            0x40000000: gpio_ctrl,
            0x40000004: gpio_data,
            0x40000008: gpio_status,
            0x4000000C: gpio_config,
            0x40000010: gpio_command
        }

    # =========================================================
    # LOOKUP
    # =========================================================

    def _get_register(self, address):
        if address not in self.registers:
            raise RegisterNotFoundError(
                f"No register exists at "
                f"address 0x{address:08X}."
            )

        return self.registers[address]

    def get_register_name(self, address):
        return self._get_register(address).name

    # =========================================================
    # READ / WRITE
    # =========================================================

    def read(self, address):
        return self._get_register(address).read()

    def write(self, address, value):
        self._get_register(address).write(value)

    def reset(self, address):
        self._get_register(address).reset()

    # =========================================================
    # BITS
    # =========================================================

    def set_bit(self, address, bit):
        self._get_register(address).set_bit(bit)

    def clear_bit(self, address, bit):
        self._get_register(address).clear_bit(bit)

    def toggle_bit(self, address, bit):
        self._get_register(address).toggle_bit(bit)

    def is_bit_set(self, address, bit):
        return self._get_register(
            address
        ).is_bit_set(bit)

    # =========================================================
    # FIELDS
    # =========================================================

    def read_field(
        self,
        address,
        field_name
    ):
        return self._get_register(
            address
        ).read_field(field_name)

    def write_field(
        self,
        address,
        field_name,
        value
    ):
        self._get_register(
            address
        ).write_field(
            field_name,
            value
        )