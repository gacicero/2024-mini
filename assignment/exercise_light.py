<<<<<<< HEAD
#!/usr/bin/env python3
"""
Use analog input with photocell
"""

import time
import machine

# GP28 is ADC2
ADC2 = 28

led = machine.Pin("LED", machine.Pin.OUT)
adc = machine.ADC(ADC2)

blink_period = 0.1

max_bright = 20000
min_bright = 10000


def clip(value: float) -> float:
    """clip number to range [0, 1]"""
    if value < 0:
        return 0
    if value > 1:
        return 1
    return value


while True:
    value = adc.read_u16()
    print(value)
    """
    need to clip duty cycle to range [0, 1]
    this equation will give values outside the range [0, 1]
    So we use function clip()
    """

    duty_cycle = clip((value - min_bright) / (max_bright - min_bright))

    led.high()
    time.sleep(blink_period * duty_cycle)

    led.low()
    time.sleep(blink_period * (1 - duty_cycle))
=======
from machine import Pin, ADC, PWM
import time

# Set up ADC for light sensor (on GP28)
adc2 = ADC(28)

# Set up PWM for LED control (on GP15, for example)
led = PWM(Pin(15))  # Use any valid PWM pin
led.freq(1000)  # Set the frequency to 1 kHz (adjust as needed)

# Brightness calibration
max_bright = 54500
min_bright = 5000

while True:
    # Read light sensor value
    light = adc2.read_u16()  # Get ADC reading (0-65535)

    # Map light value to duty cycle range for PWM
    duty_cycle = int((light - min_bright) / (max_bright - min_bright) * 65535)
    duty_cycle = max(0, min(65535, duty_cycle))  # Ensure it's between 0 and 65535

    # Set the LED brightness
    led.duty_u16(duty_cycle)  # Set the PWM duty cycle (0-65535)

    # Debug output
    print(f"Sensor value: {light}, Duty cycle: {duty_cycle}")
    
    # Sleep for a second before the next reading
    time.sleep(1)
>>>>>>> 5ac85dc1ba457c3dabb2750a2be9a98883de4c16
