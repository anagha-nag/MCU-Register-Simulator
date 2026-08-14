import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from gpio import GPIO


def main():
    gpio = GPIO()

    print("=== MCU Register Simulator Demo ===")

    print("\nInitial GPIO_CTRL:")
    print(
        hex(
            gpio.get_register_map().read(
                GPIO.GPIO_CTRL
            )
        )
    )

    print("\nConfiguring GPIO output...")
    gpio.configure_output()

    print("Setting GPIO3...")
    gpio.set_pin(3)

    print(
        "GPIO DATA:",
        hex(
            gpio.get_register_map().read(
                GPIO.GPIO_DATA
            )
        )
    )

    print("\nSetting GPIO5...")
    gpio.set_pin(5)

    print(
        "GPIO DATA:",
        hex(
            gpio.get_register_map().read(
                GPIO.GPIO_DATA
            )
        )
    )

    print("\nClearing GPIO3...")
    gpio.clear_pin(3)

    print(
        "GPIO DATA:",
        hex(
            gpio.get_register_map().read(
                GPIO.GPIO_DATA
            )
        )
    )


if __name__ == "__main__":
    main()