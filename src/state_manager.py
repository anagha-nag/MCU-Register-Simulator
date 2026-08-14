import json


class StateManager:
    """Save and load MCU simulator state."""

    def save_state(self, gpio, filename):
        """Save the current GPIO/register state to JSON."""

        register_data = {}

        for address, register in gpio.get_register_map().registers.items():
            register_data[f"0x{address:08X}"] = {
                "name": register.name,
                "value": register.value
            }

        state = {
            "registers": register_data,
            "pins": list(gpio.pins)
        }

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                state,
                file,
                indent=4
            )

    def load_state(self, gpio, filename):
        """Load GPIO/register state from JSON."""

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            state = json.load(file)

        register_map = gpio.get_register_map()

        for address_text, register_data in state["registers"].items():

            address = int(
                address_text,
                16
            )

            if address in register_map.registers:
                register_map.registers[address].value = (
                    register_data["value"]
                    & 0xFFFFFFFF
                )

        loaded_pins = state.get("pins", [])

        for index in range(
            min(
                len(loaded_pins),
                gpio.NUM_PINS
            )
        ):
            gpio.pins[index] = (
                1 if loaded_pins[index] else 0
            )