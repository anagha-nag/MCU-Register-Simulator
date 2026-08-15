import sys
from pathlib import Path
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from gpio import GPIO
from state_manager import StateManager


class TestStateManager(unittest.TestCase):

    def setUp(self):
        self.gpio = GPIO()
        self.gpio.configure_output()

        self.manager = StateManager()

    def test_save_and_load_state(self):

        self.gpio.enable()
        self.gpio.set_pin(3)
        self.gpio.set_pin(5)

        self.gpio.get_register_map().write(
            GPIO.GPIO_CTRL,
            0x51
        )

        with tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False
        ) as file:
            filename = file.name

        try:
            self.manager.save_state(
                self.gpio,
                filename
            )

            new_gpio = GPIO()
            new_gpio.configure_output()

            self.manager.load_state(
                new_gpio,
                filename
            )

            self.assertEqual(
                new_gpio.get_register_map().read(
                    GPIO.GPIO_CTRL
                ),
                0x51
            )

            self.assertEqual(
                new_gpio.pins[3],
                1
            )

            self.assertEqual(
                new_gpio.pins[5],
                1
            )

        finally:
            Path(filename).unlink(
                missing_ok=True
            )


if __name__ == "__main__":
    unittest.main()