from machine import Pin
import time
import random
import json

N: int = 10  # Changed to 10 flashes
sample_ms = 10.0
on_ms = 500

def random_time_interval(tmin: float, tmax: float) -> float:
    """Return a random time interval between max and min"""
    return random.uniform(tmin, tmax)

def blinker(N: int, led: Pin) -> None:
    """Blink LED N times to signal start/end of the game"""
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)

def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file."""
    with open(json_filename, "w") as f:
        json.dump(data, f)

def scorer(t: list[int | None]) -> None:
    """Compute and display the game scores and response times"""
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if len(t_good) > 0:
        avg_time = sum(t_good) / len(t_good)
        min_time = min(t_good)
        max_time = max(t_good)
        score = len(t_good) / len(t)
        
        print(f"Average response time: {avg_time} ms")
        print(f"Minimum response time: {min_time} ms")
        print(f"Maximum response time: {max_time} ms")
        print(f"Score: {score * 100:.2f}%")

        # Store results in a dictionary
        data = {
            "average_response_time": avg_time,
            "minimum_response_time": min_time,
            "maximum_response_time": max_time,
            "score": score
        }
    else:
        data = {
            "average_response_time": None,
            "minimum_response_time": None,
            "maximum_response_time": None,
            "score": 0
        }

    # Write data to JSON with a dynamic filename
    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"
    print("write", filename)
    write_json(filename, data)

if __name__ == "__main__":
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    # Signal game start with 3 blinks
    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()
        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)
        led.low()

    # Signal game end with 5 blinks
    blinker(5, led)

    # Compute and display scores
    scorer(t)
