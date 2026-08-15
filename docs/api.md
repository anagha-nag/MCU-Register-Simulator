# MCU Simulator API

## Overview

The `MCU` class provides a simple high-level interface for interacting
with the MCU Register Simulator.

Instead of directly interacting with `RegisterMap`, `Register32`, GPIO,
and the interrupt controller, an application can use the `MCU` API.

---

## Importing the API

```python
from mcu_api import MCU