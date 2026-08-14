# MCU Register Map

The simulator contains the following memory-mapped registers.

| Address | Register | Access | Reset |
|---|---|---|---|
| 0x40000000 | GPIO_CTRL | RW | 0x00000000 |
| 0x40000004 | GPIO_DATA | RW | 0x00000000 |
| 0x40000008 | GPIO_STATUS | RO | 0x00000001 |
| 0x4000000C | GPIO_CONFIG | RW | 0x00000010 |
| 0x40000010 | GPIO_COMMAND | WO | 0x00000000 |

## GPIO_CTRL

| Field | Bits | Description |
|---|---:|---|
| ENABLE | 0 | Enables GPIO |
| MODE | 7:4 | GPIO operating mode |

## GPIO_STATUS

| Field | Bits | Description |
|---|---:|---|
| READY | 0 | Peripheral ready status |
| ERROR | 1 | Error flag |

## GPIO_DATA

Bits 0-7 represent GPIO0-GPIO7.

Example:

```text
0x00000005