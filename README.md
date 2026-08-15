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