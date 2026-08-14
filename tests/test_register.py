import sys
from pathlib import Path
import unittest

# Add the src folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))
from access import RegisterAccess
from register import Register32
from register_map import RegisterMap
from gpio import GPIO


class TestRegister32(unittest.TestCase):

    def setUp(self):
        self.register = Register32("TEST", 0)

    def test_initial_value(self):
        self.assertEqual(self.register.read(), 0)

    def test_write_value(self):
        self.register.write(0x12345678)
        self.assertEqual(self.register.read(), 0x12345678)

    def test_write_keeps_32_bits(self):
        self.register.write(0xFFFFFFFFFF)
        self.assertEqual(self.register.read(), 0xFFFFFFFF)

    def test_set_bit(self):
        self.register.set_bit(3)
        self.assertEqual(self.register.read(), 0b1000)

    def test_clear_bit(self):
        self.register.write(0b1111)
        self.register.clear_bit(1)
        self.assertEqual(self.register.read(), 0b1101)

    def test_toggle_bit(self):
        self.register.write(0b0001)

        self.register.toggle_bit(0)
        self.assertEqual(self.register.read(), 0)

        self.register.toggle_bit(0)
        self.assertEqual(self.register.read(), 1)

    def test_is_bit_set(self):
        self.register.write(0b1000)

        self.assertTrue(self.register.is_bit_set(3))
        self.assertFalse(self.register.is_bit_set(2))

    def test_invalid_bit_low(self):
        with self.assertRaises(ValueError):
            self.register.set_bit(-1)

    def test_invalid_bit_high(self):
        with self.assertRaises(ValueError):
            self.register.set_bit(32)

    def test_invalid_bit_type(self):
        with self.assertRaises(TypeError):
            self.register.set_bit("3")

    def test_invalid_register_value(self):
        with self.assertRaises(TypeError):
            self.register.write("123")


class TestRegisterMap(unittest.TestCase):

    def setUp(self):
        self.mcu = RegisterMap()

    def test_register_exists(self):
        self.assertEqual(
            self.mcu.get_register_name(0x40000000),
            "GPIO_CTRL"
        )

    def test_initial_register_value(self):
        self.assertEqual(
            self.mcu.read(0x40000000),
            0
        )

    def test_write_and_read(self):
        self.mcu.write(0x40000004, 0x12345678)

        self.assertEqual(
            self.mcu.read(0x40000004),
            0x12345678
        )

    def test_set_bit(self):
        self.mcu.set_bit(0x40000000, 3)

        self.assertEqual(
            self.mcu.read(0x40000000),
            0x8
        )

    def test_clear_bit(self):
        self.mcu.write(0x40000000, 0xF)
        self.mcu.clear_bit(0x40000000, 1)

        self.assertEqual(
            self.mcu.read(0x40000000),
            0xD
        )

    def test_toggle_bit(self):
        self.mcu.write(0x40000000, 0x1)
        self.mcu.toggle_bit(0x40000000, 0)

        self.assertEqual(
            self.mcu.read(0x40000000),
            0
        )

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            self.mcu.read(0x50000000)


class TestRegisterFields(unittest.TestCase):

    def setUp(self):
        self.mcu = RegisterMap()
        self.gpio_ctrl = 0x40000000

    def test_write_field(self):
        self.mcu.write_field(
            self.gpio_ctrl,
            "ENABLE",
            1
        )

        self.assertEqual(
            self.mcu.read(self.gpio_ctrl),
            0x1
        )

    def test_write_multi_bit_field(self):
        self.mcu.write_field(
            self.gpio_ctrl,
            "MODE",
            5
        )

        self.assertEqual(
            self.mcu.read(self.gpio_ctrl),
            0x50
        )

    def test_read_field(self):
        self.mcu.write(
            self.gpio_ctrl,
            0x51
        )

        self.assertEqual(
            self.mcu.read_field(
                self.gpio_ctrl,
                "ENABLE"
            ),
            1
        )

        self.assertEqual(
            self.mcu.read_field(
                self.gpio_ctrl,
                "MODE"
            ),
            5
        )

    def test_field_does_not_modify_other_bits(self):
        self.mcu.write(
            self.gpio_ctrl,
            0x80000000
        )

        self.mcu.write_field(
            self.gpio_ctrl,
            "MODE",
            5
        )

        self.assertEqual(
            self.mcu.read(self.gpio_ctrl),
            0x80000050
        )

    def test_invalid_field_value(self):
        with self.assertRaises(ValueError):
            self.mcu.write_field(
                self.gpio_ctrl,
                "MODE",
                16
            )

    def test_invalid_field(self):
        with self.assertRaises(ValueError):
            self.mcu.write_field(
                self.gpio_ctrl,
                "UNKNOWN",
                1
            )
class TestRegisterAccessAndReset(unittest.TestCase):

    def test_reset_value(self):
        register = Register32(
            "TEST",
            reset_value=0x12345678
        )

        self.assertEqual(
            register.read(),
            0x12345678
        )

    def test_reset_restores_value(self):
        register = Register32(
            "TEST",
            reset_value=0x10
        )

        register.write(0xFFFFFFFF)
        register.reset()

        self.assertEqual(
            register.read(),
            0x10
        )

    def test_read_write_access(self):
        register = Register32(
            "TEST",
            access=RegisterAccess.READ_WRITE
        )

        register.write(0x55)

        self.assertEqual(
            register.read(),
            0x55
        )

    def test_read_only_read(self):
        register = Register32(
            "STATUS",
            reset_value=0x01,
            access=RegisterAccess.READ_ONLY
        )

        self.assertEqual(
            register.read(),
            0x01
        )

    def test_read_only_write_blocked(self):
        register = Register32(
            "STATUS",
            access=RegisterAccess.READ_ONLY
        )

        with self.assertRaises(PermissionError):
            register.write(0x55)

    def test_write_only_write(self):
        register = Register32(
            "COMMAND",
            access=RegisterAccess.WRITE_ONLY
        )

        register.write(0xAA)

    def test_write_only_read_blocked(self):
        register = Register32(
            "COMMAND",
            access=RegisterAccess.WRITE_ONLY
        )

        register.write(0xAA)

        with self.assertRaises(PermissionError):
            register.read()

    def test_invalid_access_type(self):
        with self.assertRaises(TypeError):
            Register32(
                "TEST",
                access="READ_ONLY"
            ) 

    def test_reset_method_on_read_only_register(self):
        register = Register32(
            "STATUS",
            reset_value=0x01,
            access=RegisterAccess.READ_ONLY
        )

        # reset should still work
        register.reset()

        self.assertEqual(
            register.read(),
            0x01
        )

    def test_reset_method_on_write_only_register(self):
        register = Register32(
            "COMMAND",
            reset_value=0x10,
            access=RegisterAccess.WRITE_ONLY
        )

        register.write(0xFF)
        register.reset()

        # We cannot call read() because this register is write-only.
        # Instead, check the internal value directly.
        self.assertEqual(
            register.value,
            0x10
        )

class TestGPIO(unittest.TestCase):

    def setUp(self):
        self.gpio = GPIO()

    def test_gpio_starts_ready(self):
        self.assertTrue(self.gpio.is_ready())

    def test_gpio_starts_without_error(self):
        self.assertFalse(self.gpio.has_error())

    def test_enable(self):
        self.gpio.enable()

        self.assertEqual(
            self.gpio.registers.read_field(
                GPIO.GPIO_CTRL,
                GPIO.ENABLE_FIELD
            ),
            1
        )

    def test_disable(self):
        self.gpio.enable()
        self.gpio.disable()

        self.assertEqual(
            self.gpio.registers.read_field(
                GPIO.GPIO_CTRL,
                GPIO.ENABLE_FIELD
            ),
            0
        )

    def test_output_mode(self):
        self.gpio.configure_output()

        self.assertEqual(
            self.gpio.registers.read_field(
                GPIO.GPIO_CTRL,
                GPIO.MODE_FIELD
            ),
            GPIO.OUTPUT_MODE
        )

    def test_set_pin(self):
        self.gpio.configure_output()

        self.gpio.set_pin(3)

        self.assertEqual(
            self.gpio.read_pin(3),
            1
        )

        self.assertEqual(
            self.gpio.read_port(),
            0x08
        )

    def test_clear_pin(self):
        self.gpio.configure_output()

        self.gpio.set_pin(3)
        self.gpio.clear_pin(3)

        self.assertEqual(
            self.gpio.read_pin(3),
            0
        )

        self.assertEqual(
            self.gpio.read_port(),
            0
        )

    def test_toggle_pin(self):
        self.gpio.configure_output()

        self.gpio.set_pin(2)
        self.gpio.toggle_pin(2)

        self.assertEqual(
            self.gpio.read_pin(2),
            0
        )

    def test_write_port(self):
        self.gpio.configure_output()

        self.gpio.write_port(0xAA)

        self.assertEqual(
            self.gpio.read_port(),
            0xAA
        )

        self.assertEqual(
            self.gpio.read_pin(1),
            1
        )

        self.assertEqual(
            self.gpio.read_pin(0),
            0
        )

    def test_disabled_gpio_blocks_operation(self):
        with self.assertRaises(RuntimeError):
            self.gpio.set_pin(0)

        self.assertTrue(
            self.gpio.has_error()
        )

    def test_input_mode_blocks_output(self):
        self.gpio.configure_input()

        with self.assertRaises(RuntimeError):
            self.gpio.set_pin(0)

        self.assertTrue(
            self.gpio.has_error()
        )

    def test_invalid_pin_low(self):
        self.gpio.configure_output()

        with self.assertRaises(ValueError):
            self.gpio.set_pin(-1)

    def test_invalid_pin_high(self):
        self.gpio.configure_output()

        with self.assertRaises(ValueError):
            self.gpio.set_pin(8)

    def test_invalid_pin_type(self):
        self.gpio.configure_output()

        with self.assertRaises(TypeError):
            self.gpio.set_pin("3")

    def test_clear_error(self):
        try:
            self.gpio.set_pin(0)
        except RuntimeError:
            pass

        self.assertTrue(
            self.gpio.has_error()
        )

        self.gpio.clear_error()

        self.assertFalse(
            self.gpio.has_error()
        )
if __name__ == "__main__":
    unittest.main()