# Exercise 3: Reaction Time Game with Microcontroller and API Integration

This project implements a reaction time game using a microcontroller (such as a Raspberry Pi Pico W). The game involves an LED that flashes for random intervals, and the user must press a button as quickly as possible. The response times are recorded, analyzed, and stored in a remote API. Users can register and log in to the system, and their game data will be saved under their account. The game also includes a scoring system to track how well the user performs in terms of response times.

The microcontroller connects to a Wi-Fi network to communicate with a Flask API for user authentication and data storage. The API sends calls to the Google Cloud Firestore and Firebase Authentication APIs in order to store each user's login information and performance data, including the average, minimum, and maximum reaction times, as well as a success score. The Flask API is hosted on Google Cloud Run and has rate-limiting implemented.

## Features

- **LED Blinking Game**: The LED flashes randomly, and the user must press a button as quickly as possible to stop it.
- **Scoring System**: The game tracks the number of missed button presses and calculates the average, minimum, and maximum reaction times. It also generates a success score based on how well the user responds during the game.
- **User Authentication**: Users can register and log in, with each game session's data stored securely under their account.
- **Data Storage**: After playing the game, the response times and scores are sent to a remote API and stored in the user's account.
- **Wi-Fi Connectivity**: The microcontroller connects to a Wi-Fi network to send data to the API.

## Challenges

- **Google Cloud Firestore**: It took a while to understand how to connect to the Cloud Firestore API from our own API.
- **Creation of a Flask API and Google Cloud Run Hosting**: We made this decision to offer a seamless and scalable backend that operated with good practice (through an intermediate API). Hosting our API on Google Cloud Run took a bit of reading documentation but we were eventually successful.
- **Google Firebase Authentication**: We flipped around numerous designs, one of which even outputted a link that users would click to open their browser. Due to the time and hardware constraints, however, we realized we could not run some of these libraries on the microcontroller's MicroPython environment, and we instead opted to use a simpler Firebase Authentication with Email/Password verification (manually checking for GMail or EDU addresses).

## Project Structure

- **random_time_interval(tmin: float, tmax: float)**: Generates a random time interval between the specified minimum and maximum values.
- **blinker(N: int, led: Pin)**: Blinks the LED N times to signal the start or end of the game.
- **scorer(t: list[int | None])**: Calculates the score and response time statistics, stores the results in a JSON object, and returns it. This function computes the average, minimum, and maximum response times based on the game results and handles any missed button presses.
- **game()**: Main logic for running the reaction time game. The game runs for a specified number of rounds (N rounds), where the LED flashes for random durations, and the user must press the button. The function returns the computed statistics (average time, minimum time, maximum time, score).
- **register_user()**: Allows a new user to register with the remote API by providing an email (restricted to Gmail) and password.
- **login_user()**: Allows an existing user to log in by providing their email and password, returning an authentication token (id_token) if successful.
- **send_data_to_api(id_token: str, data: dict)**: Sends the user's game data (response times and score) to the API using the authentication token for authorization.
- **get_user_data(id_token: str)**: Fetches and displays the stored game data (average, minimum, and maximum response times, and score) for the logged-in user from the API.
- **print_ascii_box()**: Prints a simple ASCII box on the console to indicate that the game is running.
- **main()**: Main program loop that handles Wi-Fi connection, user authentication, and running the game. After connecting to Wi-Fi, the user is prompted to log in or register. Once authenticated, they can choose to view stored data, play the game, or log out.
- This project also integrates GitHub Actions, so that whenever we make changes to the structure of the API, we can simply push the file (assignment/app.py) to this repository, and a Docker image will be built, pushed to Google Artifact Registry (GAR), and executed, so that the API will be continuously running with fresh changes. In this way, we have implemented a simple (no testing environment) CI/CD pipeline for our API.

## Getting Started

### Requirements

To run this project, you need the following:

- A microcontroller with Wi-Fi capability, such as a Raspberry Pi Pico W.
- A push button connected to a GPIO pin.
- An LED (or the onboard LED) connected to a GPIO pin.
- A Firebase API key.
- A Wi-Fi network with internet access for the microcontroller to connect to the API.

### Hardware Setup

1. Connect an LED to one of the GPIO pins on the microcontroller. If you are using the onboard LED of the Raspberry Pi Pico W, it will be automatically assigned to the pin `"LED"`.
2. Connect a push button to another GPIO pin (e.g., GPIO Pin 16). This button will be used to register the user's response to the LED flashes.

### Software Setup

1. Clone this repository or download the project files from the repository.
   ```bash
   git clone https://github.com/gacicero/2024-mini/tree/main
