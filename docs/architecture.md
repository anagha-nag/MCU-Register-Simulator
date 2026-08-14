# MCU Register Simulator Architecture

## Overview

The MCU Register Simulator is a software-based simulation of a
32-bit microcontroller register and GPIO subsystem.

The project is divided into several layers.

## Architecture

```text
GUI
 |
 v
GPIO Peripheral
 |
 v
Register Map
 |
 v
32-bit Registers
 |
 +--> Register Fields
 |
 +--> Access Permissions
 |
 +--> Reset Values