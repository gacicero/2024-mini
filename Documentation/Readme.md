


## Hardware Game  function
Purpose: Runs the main reaction time game.
Behavior:

    Initializes the LED and button pins.
        LED is connected to the built-in LED pin.
        Button is connected to GPIO pin 16 with a pull-up resistor.
    Signals the start of the game by blinking the LED three times.
    For N iterations:
        Waits for a random time interval between 0.5 and 5.0 seconds.
        Turns the LED on and records the current time (tic).
        Waits for the user to press the button or for on_ms milliseconds to pass.
            If the button is pressed, calculates the response time and turns off the LED.
            If the time exceeds on_ms, turns off the LED and records a missed attempt (None).
    Signals the end of the game by blinking the LED five times.
    Calls the scorer function to calculate and display statistics.
    Returns the statistics dictionary

