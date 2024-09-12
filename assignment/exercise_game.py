import urequests
import json
import time
from machine import Pin
import random


API_BASE_URL = "https://flask-api-560047854310.us-east1.run.app"
REGISTER_URL = f"{API_BASE_URL}/user/register"
LOGIN_URL = f"{API_BASE_URL}/user/login"
DATA_URL = f"{API_BASE_URL}/user/data"  # Endpoint to send or retrieve user data


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

def scorer(t: list[int | None]) -> dict:
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
    return data


def game():
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
    data = scorer(t)
    return data




def register_user():
    email = input('Enter your Gmail address: ')
    if not email.endswith('@gmail.com'):
        print('Email must be a Gmail address.')
        return None

    password = input('Create a password: ')
    display_name = input('Enter your display name: ')

    data = {
        'email': email,
        'password': password,
        'display_name': display_name
    }

    try:
        response = urequests.post(REGISTER_URL, json=data)
        if response.status_code == 200:
            print('Registration successful.')
            return email, password
        else:
            print('Registration failed:', response.json().get('error'))
            return None
    except Exception as e:
        print('Error during registration:', e)
        return None

# User Login
def login_user():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    data = {
        'email': email,
        'password': password
    }

    try:
        response = urequests.post(LOGIN_URL, json=data)
        if response.status_code == 200:
            print('Login successful.')
            id_token = response.json().get('idToken')
            return email, id_token
        else:
            print('Login failed:', response.json().get('error'))
            return None
    except Exception as e:
        print('Error during login:', e)
        return None


# Send Data to API
def send_data_to_api(id_token, data):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {id_token}'
        }
        response = urequests.post(DATA_URL, headers=headers, json=data)
        if response.status_code == 200:
            print('Data sent successfully.')
        else:
            print('Failed to send data:', response.json().get('error'))
    except Exception as e:
        print('Error sending data:', e)

# Get User Data
def get_user_data(id_token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {id_token}'
        }
        response = urequests.get(DATA_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print('User Data:')
            print(f"Average response time: {data['average_response_time']} ms")
            print(f"Minimum response time: {data['minimum_response_time']} ms")
            print(f"Maximum response time: {data['maximum_response_time']} ms")
            print(f"Score: {data['score'] * 100:.2f}%")
        else:
            print('Failed to retrieve data:', response.json().get('error'))
    except Exception as e:
        print('Error fetching user data:', e)


def main():
    # Connect to Wi-Fi
    # connect_to_wifi('your-SSID', 'your-password')

    # Authentication Loop
    while True:
        print('Please choose an option:')
        print('1. Log In')
        print('2. Sign Up')
        choice = input('Enter your choice: ')

        if choice == '1':
            auth_result = login_user()
            if auth_result:
                email, id_token = auth_result
                break  # Exit loop if login is successful
        elif choice == '2':
            auth_result = register_user()
            if auth_result:
                email, password = auth_result
                # Automatically log in after successful registration
                auth_result = login_user()
                if auth_result:
                    email, id_token = auth_result
                    break
        else:
            print('Invalid choice. Please try again.')

    # Proceed to REPL loop
    while True:
        print('What would you like to do?')
        print('1. View data')
        print('2. Run test and store new data')
        print('3. Log out')
        choice = input('Enter your choice: ')

        if choice == '1':
            get_user_data(id_token)
        elif choice == '2':
            # Run your test and get data
            data = game()
            if data:
                data = json.dumps(data)
                send_data_to_api(id_token, data)
        elif choice == '3':
            print('Logging out...')
            id_token = None
            break
        else:
            print('Invalid choice. Please try again.')

    print('Goodbye!')
    return

    


if __name__ == "__main__":
    main()
