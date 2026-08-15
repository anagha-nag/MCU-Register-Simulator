import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)

from mcu_api import MCU


def main():

    print("=== MCU Public API Demo ===")

    mcu = MCU()

    print("\nSetting GPIO3...")
    mcu.set_gpio(3)

    print(
        "GPIO3:",
        mcu.read_gpio(3)
    )

    print("\nToggling GPIO3...")
    mcu.toggle_gpio(3)

    print(
        "GPIO3:",
        mcu.read_gpio(3)
    )

    print("\nWriting GPIO port...")
    mcu.write_gpio_port(0x25)

    print(
        "GPIO port:",
        hex(mcu.read_gpio_port())
    )


if __name__ == "__main__":
    main()