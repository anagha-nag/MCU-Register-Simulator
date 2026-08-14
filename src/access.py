from enum import Enum


class RegisterAccess(Enum):
    READ_WRITE = "RW"
    READ_ONLY = "RO"
    WRITE_ONLY = "WO"