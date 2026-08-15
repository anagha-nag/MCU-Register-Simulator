import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)

from errors import (
    GPIOPinError,
    GPIOConfigurationError,
    RegisterNotFoundError
)

from gpio import GPIO
from register_map import RegisterMap


class TestErrorHandling(unittest.TestCase):

    def test_invalid_gpio_pin(self):
        gpio = GPIO()

        with self.assertRaises(
            GPIOPinError
        ):
            gpio.set_pin(8)

    def test_negative_gpio_pin(self):
        gpio = GPIO()

        with self.assertRaises(
            GPIOPinError
        ):
            gpio.set_pin(-1)

    def test_invalid_register_address(self):
        register_map = RegisterMap()

        with self.assertRaises(
            RegisterNotFoundError
        ):
            register_map.read(
                0x50000000
            )

    def test_gpio_disabled(self):
        gpio = GPIO()

        gpio.disable()

        with self.assertRaises(
            GPIOConfigurationError
        ):
            gpio.set_pin(3)


if __name__ == "__main__":
    unittest.main()