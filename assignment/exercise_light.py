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
