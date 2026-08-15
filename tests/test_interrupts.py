import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from gpio import GPIO
from interrupt_controller import InterruptController
from event_manager import EventManager


class TestInterruptController(unittest.TestCase):

    def setUp(self):
        self.controller = InterruptController()

        self.controller.register_interrupt(
            "TEST"
        )

    def test_interrupt_starts_disabled(self):
        self.assertFalse(
            self.controller.is_enabled("TEST")
        )

    def test_interrupt_starts_not_pending(self):
        self.assertFalse(
            self.controller.is_pending("TEST")
        )

    def test_enable_interrupt(self):
        self.controller.enable_interrupt(
            "TEST"
        )

        self.assertTrue(
            self.controller.is_enabled("TEST")
        )

    def test_disable_interrupt(self):
        self.controller.enable_interrupt(
            "TEST"
        )

        self.controller.disable_interrupt(
            "TEST"
        )

        self.assertFalse(
            self.controller.is_enabled("TEST")
        )

    def test_raise_interrupt_sets_pending(self):
        self.controller.raise_interrupt(
            "TEST"
        )

        self.assertTrue(
            self.controller.is_pending("TEST")
        )

    def test_trigger_count(self):
        self.controller.raise_interrupt("TEST")
        self.controller.raise_interrupt("TEST")
        self.controller.raise_interrupt("TEST")

        self.assertEqual(
            self.controller.get_trigger_count("TEST"),
            3
        )

    def test_clear_pending(self):
        self.controller.raise_interrupt(
            "TEST"
        )

        self.assertTrue(
            self.controller.is_pending("TEST")
        )

        self.controller.clear_pending(
            "TEST"
        )

        self.assertFalse(
            self.controller.is_pending("TEST")
        )

    def test_service_disabled_interrupt(self):
        received = []

        def handler(data):
            received.append(data)

        self.controller.attach_handler(
            "TEST",
            handler
        )

        self.controller.raise_interrupt(
            "TEST",
            {"value": 5}
        )

        serviced = self.controller.service_interrupt(
            "TEST",
            {"value": 5}
        )

        self.assertFalse(
            serviced
        )

        self.assertTrue(
            self.controller.is_pending("TEST")
        )

        self.assertEqual(
            received,
            []
        )

    def test_service_enabled_interrupt(self):
        received = []

        def handler(data):
            received.append(data)

        self.controller.attach_handler(
            "TEST",
            handler
        )

        self.controller.enable_interrupt(
            "TEST"
        )

        self.controller.raise_interrupt(
            "TEST",
            {"value": 10}
        )

        serviced = self.controller.service_interrupt(
            "TEST",
            {"value": 10}
        )

        self.assertTrue(
            serviced
        )

        self.assertFalse(
            self.controller.is_pending("TEST")
        )

        self.assertEqual(
            received,
            [{"value": 10}]
        )

    def test_invalid_interrupt(self):
        with self.assertRaises(ValueError):
            self.controller.enable_interrupt(
                "UNKNOWN"
            )

    def test_invalid_handler(self):
        with self.assertRaises(TypeError):
            self.controller.attach_handler(
                "TEST",
                "not a function"
            )


class TestEventManager(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()

    def test_event_subscription(self):
        received = []

        def callback(data):
            received.append(data)

        self.manager.subscribe(
            "TEST",
            callback
        )

        self.manager.publish(
            "TEST",
            123
        )

        self.assertEqual(
            received,
            [123]
        )

    def test_multiple_subscribers(self):
        received = []

        def callback_one(data):
            received.append(
                ("one", data)
            )

        def callback_two(data):
            received.append(
                ("two", data)
            )

        self.manager.subscribe(
            "TEST",
            callback_one
        )

        self.manager.subscribe(
            "TEST",
            callback_two
        )

        self.manager.publish(
            "TEST",
            50
        )

        self.assertEqual(
            received,
            [
                ("one", 50),
                ("two", 50)
            ]
        )

    def test_unsubscribe(self):
        received = []

        def callback(data):
            received.append(data)

        self.manager.subscribe(
            "TEST",
            callback
        )

        self.manager.unsubscribe(
            "TEST",
            callback
        )

        self.manager.publish(
            "TEST",
            99
        )

        self.assertEqual(
            received,
            []
        )


class TestGPIOInterrupts(unittest.TestCase):

    def setUp(self):
        self.gpio = GPIO()
        self.gpio.configure_output()

    def test_all_gpio_interrupts_exist(self):
        for pin in range(8):
            self.assertFalse(
                self.gpio.is_interrupt_enabled(pin)
            )

    def test_enable_pin_interrupt(self):
        self.gpio.enable_pin_interrupt(3)

        self.assertTrue(
            self.gpio.is_interrupt_enabled(3)
        )

    def test_disable_pin_interrupt(self):
        self.gpio.enable_pin_interrupt(3)
        self.gpio.disable_pin_interrupt(3)

        self.assertFalse(
            self.gpio.is_interrupt_enabled(3)
        )

    def test_gpio_change_creates_pending_interrupt(self):
        self.gpio.enable_pin_interrupt(3)

        self.gpio.set_pin(3)

        self.assertTrue(
            self.gpio.is_interrupt_pending(3)
        )

    def test_gpio_change_increments_count(self):
        self.gpio.enable_pin_interrupt(3)

        self.gpio.set_pin(3)
        self.gpio.clear_pin(3)
        self.gpio.set_pin(3)

        self.assertEqual(
            self.gpio.get_interrupt_count(3),
            3
        )

    def test_clear_gpio_interrupt(self):
        self.gpio.enable_pin_interrupt(3)

        self.gpio.set_pin(3)

        self.assertTrue(
            self.gpio.is_interrupt_pending(3)
        )

        self.gpio.clear_interrupt(3)

        self.assertFalse(
            self.gpio.is_interrupt_pending(3)
        )

    def test_service_gpio_interrupt(self):
        received = []

        def handler(event):
            received.append(event)

        self.gpio.attach_pin_interrupt_handler(
            3,
            handler
        )

        self.gpio.enable_pin_interrupt(3)

        self.gpio.set_pin(3)

        self.assertTrue(
            self.gpio.is_interrupt_pending(3)
        )

        serviced = self.gpio.service_interrupt(3)

        self.assertTrue(
            serviced
        )

        self.assertFalse(
            self.gpio.is_interrupt_pending(3)
        )

        self.assertEqual(
            received[0]["pin"],
            3
        )

        self.assertEqual(
            received[0]["state"],
            1
        )

    def test_different_gpio_pins_have_separate_interrupts(self):
        self.gpio.enable_pin_interrupt(2)
        self.gpio.enable_pin_interrupt(5)

        self.gpio.set_pin(2)

        self.assertTrue(
            self.gpio.is_interrupt_pending(2)
        )

        self.assertFalse(
            self.gpio.is_interrupt_pending(5)
        )

    def test_write_port_only_raises_changed_pin_interrupts(self):
        self.gpio.enable_pin_interrupt(0)
        self.gpio.enable_pin_interrupt(1)
        self.gpio.enable_pin_interrupt(2)

        self.gpio.write_port(0b00000101)

        self.assertTrue(
            self.gpio.is_interrupt_pending(0)
        )

        self.assertFalse(
            self.gpio.is_interrupt_pending(1)
        )

        self.assertTrue(
            self.gpio.is_interrupt_pending(2)
        )


if __name__ == "__main__":
    unittest.main()