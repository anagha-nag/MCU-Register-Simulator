# MCU Register Simulator

A software-based 32-bit microcontroller register and GPIO simulator
developed in Python.

The project models memory-mapped registers, register fields, GPIO
behavior, interrupts, events, access permissions, state persistence,
and an interactive debugging interface.

---

## Project Overview

The MCU Register Simulator provides a software environment for
experimenting with concepts commonly used in embedded software
development.

Instead of requiring physical MCU hardware, the project simulates:

- 32-bit memory-mapped registers
- Register fields and bit manipulation
- Read-only, write-only, and read/write access
- Register reset behavior
- GPIO peripheral operation
- GPIO input/output modes
- GPIO pin state changes
- Interrupt generation and servicing
- Event notifications
- Operation history
- Simulator state save/load
- Custom error handling
- A high-level MCU API
- An interactive graphical interface

---

## Architecture

```text
                    MCU Register Simulator
                             |
              +--------------+--------------+
              |                             |
              v                             v
             GUI                         MCU API
              |                             |
              +--------------+--------------+
                             |
                             v
                            GPIO
                             |
            +----------------+----------------+
            |                |                |
            v                v                v
       RegisterMap    EventManager    InterruptController
            |
            v
        Register32
            |
            v
      RegisterField

## Key Features

* 32-bit memory-mapped register simulation
* Register fields and bit-level manipulation
* Read-only, write-only, and read/write access permissions
* Register reset behavior
* GPIO peripheral simulation
* GPIO pin state control
* GPIO port read/write operations
* GPIO interrupt generation and servicing
* Event management and notifications
* Interrupt controller
* Operation history
* Simulator state persistence
* Custom error handling
* High-level MCU API
* Interactive graphical user interface
* Example applications
* Automated unit testing

---

## Project Structure

```text
MCU-Register-Simulator/
├── docs/
│   └── api.md
├── examples/
│   ├── api_demo.py
│   ├── gpio_application.py
│   └── interrupt_demo.py
├── src/
│   ├── errors.py
│   ├── event_manager.py
│   ├── gpio.py
│   ├── gui.py
│   ├── interrupt_controller.py
│   ├── mcu_api.py
│   ├── register.py
│   ├── register_field.py
│   └── register_map.py
├── tests/
│   ├── test_application.py
│   ├── test_errors.py
│   ├── test_interrupts.py
│   └── test_state_manager.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Directory Description

| Directory/File     | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `src/`             | Core MCU simulator implementation                    |
| `tests/`           | Automated test suite                                 |
| `examples/`        | Example applications demonstrating the simulator API |
| `docs/`            | API documentation                                    |
| `requirements.txt` | Python dependencies                                  |
| `README.md`        | Project documentation                                |

---

## Technologies Used

### Programming & Software Development

* Python
* Object-Oriented Programming
* Modular software design
* Exception handling
* Unit testing

### Embedded Systems Concepts

* MCU register architecture
* 32-bit registers
* Register fields
* Bit manipulation
* Memory-mapped registers
* GPIO
* Interrupt handling
* Event management
* Register access permissions
* State management

### Application & Interface

* High-level API design
* Command-line example applications
* Graphical user interface development
* Automated testing

---

## Getting Started

### Prerequisites

* Python 3.x
* Git
* A terminal or command-line environment

### Clone the Repository

```bash
git clone https://github.com/anagha-nag/MCU-Register-Simulator.git
cd MCU-Register-Simulator
```

### Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

The simulator provides a high-level `MCU` API that applications can use to interact with simulated GPIO and other MCU functionality.

### Basic API Example

```python
from mcu_api import MCU

mcu = MCU()

mcu.set_gpio(3)
print(mcu.read_gpio(3))

mcu.toggle_gpio(3)

mcu.write_gpio_port(0x25)
print(hex(mcu.read_gpio_port()))
```

A complete API demonstration is available in:

[`examples/api_demo.py`](examples/api_demo.py)

---

## Example Application

The project includes an interactive GPIO application built using the public MCU API.

The application demonstrates:

* GPIO initialization
* GPIO pin configuration
* Setting GPIO pins HIGH
* Clearing GPIO pins
* Toggling GPIO pins
* GPIO port read/write operations
* GPIO interrupt configuration
* Interrupt status monitoring
* Interrupt servicing
* GPIO interrupt event handling
* Error handling

Run the example with:

```bash
python examples/gpio_application.py
```

The application provides an interactive command menu for controlling the simulated GPIO system.

---

## Testing

The project includes an automated test suite covering application behavior, error handling, interrupts, and state management.

Run the complete test suite with:

```bash
python -m unittest discover -s tests
```

### Test Result

```text
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.020s

OK
```

**82 tests passed successfully.**

---

## Graphical User Interface

The MCU Register Simulator includes an interactive graphical interface for observing and interacting with the simulated MCU environment.

The GUI provides a visual interface for working with simulated register and peripheral behavior.

> A GUI screenshot will be added to this section.

---

## API Documentation

The project includes documentation for the public MCU API.

The API documentation explains the high-level `MCU` interface used by applications to interact with the simulator.

📖 [View MCU Simulator API Documentation](docs/api.md)

---

## Examples

The repository includes example programs demonstrating different parts of the simulator:

| Example               | Description                                    |
| --------------------- | ---------------------------------------------- |
| `api_demo.py`         | Demonstrates the high-level MCU API            |
| `gpio_application.py` | Interactive GPIO application using the MCU API |
| `interrupt_demo.py`   | Demonstrates interrupt-related functionality   |

These examples provide starting points for experimenting with the simulator.

---

## Future Improvements

Possible future extensions include:

* Additional MCU peripherals such as UART, SPI, I2C, ADC, and PWM
* More detailed peripheral register models
* Expanded interrupt and event simulation
* Enhanced GUI visualization
* Additional automated test coverage
* Configuration-based MCU definitions
* More example applications
* Extended API documentation

---

## Project Goals

The main goal of this project is to provide a software-only environment for learning and experimenting with concepts commonly used in embedded firmware development without requiring physical MCU hardware.

The simulator is designed to demonstrate how registers, peripherals, interrupts, APIs, and application-level software can interact within an MCU-oriented architecture.

