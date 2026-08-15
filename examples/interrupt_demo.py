import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)

from gpio import GPIO


def gpio3_isr(event):
    print(
        "ISR: GPIO3 changed ->",
        event
    )


def gpio_event(event):
    print(
        "EVENT: GPIO change ->",
        event
    )


def main():
    gpio = GPIO()

    gpio.configure_output()

    # Attach ISR to GPIO3.
    gpio.attach_pin_interrupt_handler(
        3,
        gpio3_isr
    )

    # Enable GPIO3 interrupt.
    gpio.enable_pin_interrupt(3)

    # Subscribe to general GPIO events.
    gpio.subscribe_event(
        "GPIO_CHANGE",
        gpio_event
    )

    print("Setting GPIO3...")
    gpio.set_pin(3)

    print("\nToggling GPIO3...")
    gpio.toggle_pin(3)

    print("\nClearing GPIO3...")
    gpio.clear_pin(3)


if __name__ == "__main__":
    main()