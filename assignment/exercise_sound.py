#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

from machine import Pin, PWM
import time

# Pin configuration for the speaker
speaker_pin = 16
speaker = PWM(Pin(speaker_pin))

# Define frequencies of musical notes (A4 = 440 Hz, C5 = 523 Hz, etc.)
note_frequencies = {
    'C4': 261,  # Middle C
    'D4': 294,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523,
}

# Define a melody (notes and duration)
melody = [
    ('C4', 0.4), ('C4', 0.4), ('G4', 0.4), ('G4', 0.4), 
    ('A4', 0.4), ('A4', 0.4), ('G4', 0.8),  # "Twinkle, Twinkle, Little Star"
    ('F4', 0.4), ('F4', 0.4), ('E4', 0.4), ('E4', 0.4), 
    ('D4', 0.4), ('D4', 0.4), ('C4', 0.8)
]

# Function to play a single tone
def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)  # Set duty cycle
    speaker.freq(frequency)  # Set frequency of the tone
    time.sleep(duration)     # Hold the tone for the given duration

# Function to turn off the speaker (quiet)
def quiet():
    speaker.duty_u16(0)

# Play the melody
for note, duration in melody:
    frequency = note_frequencies[note]
    print(f"Playing note: {note} Frequency: {frequency} Hz")
    playtone(frequency, duration)
    quiet()
    time.sleep(0.1)  # Pause between notes

quiet()  # Ensure the speaker is quiet at the end
