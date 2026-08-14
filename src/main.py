from gpio import GPIO


gpio = GPIO()


print("=== GPIO Peripheral Simulator ===")

print("\nInitial status:")
print("Ready:", gpio.is_ready())
print("Error:", gpio.has_error())


print("\nConfiguring GPIO for output...")
gpio.configure_output()

print("GPIO enabled and configured.")


print("\nSetting GPIO3 HIGH...")
gpio.set_pin(3)

print("GPIO3:", gpio.read_pin(3))
print("GPIO DATA:", hex(gpio.read_port()))


print("\nSetting GPIO0 HIGH...")
gpio.set_pin(0)

print("GPIO0:", gpio.read_pin(0))
print("GPIO DATA:", hex(gpio.read_port()))


print("\nToggling GPIO3...")
gpio.toggle_pin(3)

print("GPIO3:", gpio.read_pin(3))
print("GPIO DATA:", hex(gpio.read_port()))


print("\nClearing GPIO0...")
gpio.clear_pin(0)

print("GPIO0:", gpio.read_pin(0))
print("GPIO DATA:", hex(gpio.read_port()))


print("\nWriting entire port = 0xAA...")
gpio.write_port(0xAA)

print("GPIO DATA:", hex(gpio.read_port()))


print("\nFinal status:")
print("Ready:", gpio.is_ready())
print("Error:", gpio.has_error())
print("\nTesting error handling...")

gpio.disable()

try:
    gpio.set_pin(2)
except RuntimeError as error:
    print("Expected error:", error)

print("Error flag:", gpio.has_error())