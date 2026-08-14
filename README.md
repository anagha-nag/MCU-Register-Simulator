# MCU Register Simulator

A software-based 32-bit MCU register and GPIO simulator built with Python.

## Features

- 32-bit register model
- Memory-mapped register architecture
- Register fields and bit masks
- Read/Write access permissions
- Register reset behavior
- GPIO peripheral simulation
- Interactive GUI
- Bit-level manipulation
- Field-level editing
- Operation history
- Save/load simulator state
- Automated unit testing

## Architecture

```text
GUI
 |
 v
GPIO
 |
 v
RegisterMap
 |
 v
Register32
 |
 +--> RegisterField