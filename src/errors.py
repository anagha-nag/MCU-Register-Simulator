class MCUSimulatorError(Exception):
    """Base exception for the MCU Register Simulator."""


# =============================================================
# REGISTER ERRORS
# =============================================================

class RegisterError(MCUSimulatorError):
    """Base class for register-related errors."""


class RegisterNotFoundError(
    RegisterError,
    ValueError
):
    """Raised when a register address does not exist."""


class RegisterAccessError(
    RegisterError,
    PermissionError
):
    """Raised when register access is not permitted."""


class InvalidRegisterValueError(
    RegisterError,
    ValueError
):
    """Raised when a register value is invalid."""


# =============================================================
# REGISTER FIELD ERRORS
# =============================================================

class RegisterFieldError(RegisterError):
    """Base class for register-field errors."""


class InvalidFieldValueError(
    RegisterFieldError,
    ValueError
):
    """Raised when a field value is invalid."""


# =============================================================
# GPIO ERRORS
# =============================================================

class GPIOError(MCUSimulatorError):
    """Base class for GPIO-related errors."""


class GPIOConfigurationError(
    GPIOError,
    RuntimeError
):
    """Raised when GPIO configuration is invalid."""


class GPIOPinError(
    GPIOError,
    ValueError
):
    """Raised when a GPIO pin is invalid."""


# =============================================================
# INTERRUPT ERRORS
# =============================================================

class InterruptError(MCUSimulatorError):
    """Base class for interrupt-related errors."""


class InterruptNotFoundError(
    InterruptError,
    ValueError
):
    """Raised when an interrupt source does not exist."""


class InterruptConfigurationError(
    InterruptError,
    TypeError
):
    """Raised when interrupt configuration is invalid."""