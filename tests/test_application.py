import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)

from mcu_api import MCU


class TestMCUApplicationAPI(unittest.TestCase):

    def setUp(self):
        self.mcu = MCU()

    def test_set_gpio(self):
        self.mcu.set_gpio(3)

        self.assertEqual(
            self.mcu.read_gpio(3),
            1
        )

    def test_clear_gpio(self):
        self.mcu.set_gpio(3)
        self.mcu.clear_gpio(3)

        self.assertEqual(
            self.mcu.read_gpio(3),
            0
        )

    def test_toggle_gpio(self):
        self.mcu.set_gpio(3)

        self.mcu.toggle_gpio(3)

        self.assertEqual(
            self.mcu.read_gpio(3),
            0
        )

    def test_port_write(self):
        self.mcu.write_gpio_port(
            0x25
        )

        self.assertEqual(
            self.mcu.read_gpio_port(),
            0x25
        )

    def test_interrupt_pending(self):
        self.mcu.enable_gpio_interrupt(
            3
        )

        self.mcu.set_gpio(3)

        self.assertTrue(
            self.mcu.gpio_interrupt_pending(
                3
            )
        )


if __name__ == "__main__":
    unittest.main()