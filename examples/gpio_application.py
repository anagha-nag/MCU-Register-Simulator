import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)

from mcu_api import MCU


class GPIOApplication:
    """Example application built using the MCU public API."""

    def __init__(self):
        self.mcu = MCU()

        self._configure()

    # =========================================================
    # CONFIGURATION
    # =========================================================

    def _configure(self):
      """Configure GPIO and interrupts."""

      self.mcu.enable_gpio()

      for pin in range(8):

          self.mcu.attach_gpio_interrupt_handler(
            pin,
            self.gpio_interrupt_handler
        )

          self.mcu.enable_gpio_interrupt(
            pin
        )

    print("MCU initialized.")
    print("GPIO configured for output mode.")
    print("GPIO interrupts enabled.")

    # =========================================================
    # GPIO DISPLAY
    # =========================================================

    def display_gpio_state(self):
        """Display all GPIO pin states."""

        print("\nGPIO STATES")

        print("-" * 30)

        for pin in range(8):
            state = self.mcu.read_gpio(pin)

            state_text = (
                "HIGH"
                if state
                else "LOW"
            )

            print(
                f"GPIO{pin}: {state_text}"
            )

        print("-" * 30)

    # =========================================================
    # SET PIN
    # =========================================================

    def set_pin(self, pin):
        """Set one GPIO pin HIGH."""

        try:
            self.mcu.set_gpio(pin)

            print(
                f"GPIO{pin} set HIGH."
            )

        except Exception as error:
            print(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # CLEAR PIN
    # =========================================================

    def clear_pin(self, pin):
        """Set one GPIO pin LOW."""

        try:
            self.mcu.clear_gpio(pin)

            print(
                f"GPIO{pin} set LOW."
            )

        except Exception as error:
            print(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # TOGGLE PIN
    # =========================================================

    def toggle_pin(self, pin):
        """Toggle one GPIO pin."""

        try:
            self.mcu.toggle_gpio(pin)

            print(
                f"GPIO{pin} toggled."
            )

        except Exception as error:
            print(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # INTERRUPTS
    # =========================================================

    def service_interrupt(self, pin):
        """Service a pending GPIO interrupt."""

        try:
            pending = (
                self.mcu
                .gpio_interrupt_pending(pin)
            )

            if not pending:
                print(
                    f"No pending interrupt "
                    f"for GPIO{pin}."
                )
                return

            serviced = (
                self.mcu
                .service_gpio_interrupt(pin)
            )

            if serviced:
                print(
                    f"GPIO{pin} interrupt serviced."
                )

            else:
                print(
                    f"GPIO{pin} interrupt "
                    f"could not be serviced."
                )

        except Exception as error:
            print(
                f"INTERRUPT ERROR: {error}"
            )

    # =========================================================
    # INTERRUPT STATUS
    # =========================================================

    def show_interrupt_status(self):
        """Display pending interrupt states."""

        print("\nINTERRUPT STATUS")

        print("-" * 35)

        for pin in range(8):

            pending = (
                self.mcu
                .gpio_interrupt_pending(pin)
            )

            status = (
                "PENDING"
                if pending
                else "CLEAR"
            )

            print(
                f"GPIO{pin}_CHANGE: {status}"
            )

        print("-" * 35)

    def gpio_interrupt_handler(self, event):
      """Handle a GPIO interrupt."""

      if event is None:
        return

      pin = event["pin"]
      state = event["state"]

      print(
        f"ISR: GPIO{pin} changed to "
        f"{state}"
    )

    # =========================================================
    # MENU
    # =========================================================

    def show_menu(self):
        """Display the application menu."""

        print()
        print("=" * 45)
        print("       MCU GPIO APPLICATION")
        print("=" * 45)

        print("1. Display GPIO states")
        print("2. Set GPIO pin")
        print("3. Clear GPIO pin")
        print("4. Toggle GPIO pin")
        print("5. Show interrupt status")
        print("6. Service GPIO interrupt")
        print("7. Write GPIO port")
        print("8. Read GPIO port")
        print("9. Exit")

        print("=" * 45)

    # =========================================================
    # COMMAND LOOP
    # =========================================================

    def run(self):
        """Run the application."""

        while True:

            self.show_menu()

            choice = input(
                "Select an option: "
            ).strip()

            # -------------------------------------------------
            # DISPLAY GPIO
            # -------------------------------------------------

            if choice == "1":

                self.display_gpio_state()

            # -------------------------------------------------
            # SET
            # -------------------------------------------------

            elif choice == "2":

                try:
                    pin = int(
                        input(
                            "Enter GPIO pin (0-7): "
                        )
                    )

                    self.set_pin(pin)

                except ValueError:
                    print(
                        "Please enter a valid "
                        "integer."
                    )

            # -------------------------------------------------
            # CLEAR
            # -------------------------------------------------

            elif choice == "3":

                try:
                    pin = int(
                        input(
                            "Enter GPIO pin (0-7): "
                        )
                    )

                    self.clear_pin(pin)

                except ValueError:
                    print(
                        "Please enter a valid "
                        "integer."
                    )

            # -------------------------------------------------
            # TOGGLE
            # -------------------------------------------------

            elif choice == "4":

                try:
                    pin = int(
                        input(
                            "Enter GPIO pin (0-7): "
                        )
                    )

                    self.toggle_pin(pin)

                except ValueError:
                    print(
                        "Please enter a valid "
                        "integer."
                    )

            # -------------------------------------------------
            # INTERRUPT STATUS
            # -------------------------------------------------

            elif choice == "5":

                self.show_interrupt_status()

            # -------------------------------------------------
            # SERVICE INTERRUPT
            # -------------------------------------------------

            elif choice == "6":

                try:
                    pin = int(
                        input(
                            "Enter GPIO pin (0-7): "
                        )
                    )

                    self.service_interrupt(pin)

                except ValueError:
                    print(
                        "Please enter a valid "
                        "integer."
                    )

            # -------------------------------------------------
            # WRITE PORT
            # -------------------------------------------------

            elif choice == "7":

                try:
                    value = input(
                        "Enter GPIO value "
                        "(hex, e.g. 25): "
                    ).strip()

                    value = int(
                        value,
                        16
                    )

                    self.mcu.write_gpio_port(
                        value
                    )

                    print(
                        f"GPIO port written: "
                        f"0x{value:02X}"
                    )

                except ValueError as error:
                    print(
                        f"Invalid value: {error}"
                    )

            # -------------------------------------------------
            # READ PORT
            # -------------------------------------------------

            elif choice == "8":

                try:
                    value = (
                        self.mcu
                        .read_gpio_port()
                    )

                    print(
                        f"GPIO port: "
                        f"0x{value:02X}"
                    )

                except Exception as error:
                    print(
                        f"GPIO ERROR: {error}"
                    )

            # -------------------------------------------------
            # EXIT
            # -------------------------------------------------

            elif choice == "9":

                print(
                    "Exiting MCU GPIO Application."
                )

                break

            else:

                print(
                    "Invalid option."
                )


def main():
    application = GPIOApplication()
    application.run()


if __name__ == "__main__":
    main()