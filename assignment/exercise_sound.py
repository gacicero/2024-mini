#!/usr/bin/env python3
"""
PWM Tone Generator - London Bridge Is Falling Down

This program plays "London Bridge Is Falling Down" using PWM on a Raspberry Pi Pico.
GP16 is used to drive a speaker.

Connect the speaker's black wire (negative) to GND and the red wire (positive) to GP16.
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# Create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

# Define the frequencies for the notes (in Hz)
# Notes in the C major scale (C4, D4, E4, F4, G4, A4, B4, C5)
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25
}

# Define the melody for "London Bridge Is Falling Down"
# Each tuple is a note and its duration in seconds
london_bridge_melody = [
    ('G4', 0.5), ('A4', 0.5), ('G4', 0.5), ('F4', 0.5),  # "London Bridge is"
    ('E4', 0.5), ('F4', 0.5), ('G4', 1.0),              # "falling down,"
    
    ('E4', 0.5), ('F4', 0.5), ('G4', 0.5), ('A4', 0.5),  # "falling down,"
    ('G4', 0.5), ('F4', 0.5), ('E4', 1.0),              # "falling down,"

    ('D4', 0.5), ('E4', 0.5), ('F4', 0.5), ('E4', 0.5),  # "London Bridge is"
    ('F4', 0.5), ('G4', 0.5), ('A4', 1.0),              # "falling down,"

    ('G4', 0.5), ('A4', 0.5), ('G4', 0.5), ('F4', 0.5),  # "My fair lady."
    ('E4', 0.5), ('D4', 0.5), ('C4', 1.0)               # "My fair lady."
]

def playtone(frequency: float, duration: float) -> None:
    """Play a tone at the given frequency (Hz) for the given duration (seconds)."""
    speaker.duty_u16(1000)  # Set PWM duty cycle
    speaker.freq(int(frequency))  # Set frequency of PWM signal
    utime.sleep(duration)  # Play for the specified duration

def quiet():
    """Stop playing sound by setting the duty cycle to 0."""
    speaker.duty_u16(0)

def play_song(song):
    """Play the provided song (list of note and duration tuples)."""
    for note, duration in song:
        if note in notes:
            frequency = notes[note]
            print(f"Playing {note} ({frequency:.2f} Hz) for {duration} seconds")
            playtone(frequency, duration)
            utime.sleep(0.05)  # Short pause between notes
        else:
            quiet()  # Rest

# Play "London Bridge Is Falling Down"
play_song(london_bridge_melody)

quiet()
