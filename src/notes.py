import numpy as np
from config import *

def get_note(angle):
    if angle:
        bins = np.linspace(45, 150, 8)
        note_index = np.digitize(angle, bins)
        note_index = np.digitize(angle, bins, right=True)
        note_index -= 1
        return max(note_index, 0)


# scale is wrong. might need to shift indices each time
NOTE_IDX_TO_SEMITONES = [0, 2, 4, 5, 7, 9, 11, 12]

# Formula for calculating 12-TET frequencies:
# P_{n} = P_{a} * 2^(n/12), where P_{a} is a reference frequency (like A4=440 Hz), 
# n is the number of semitones from that reference, and 2^(1/12)
# is the constant multiplier for each half-step, dividing the octave into 12 equal logarithmic steps. 
def get_next_frequency(prev_freq, next_note_number):
    num_semitones = NOTE_IDX_TO_SEMITONES[next_note_number]
    next_freq = prev_freq * 2 ** (num_semitones/12)
    return next_freq

def get_chord_freqs(note1, note2, note3, note4):
    freqs = [BASE_FREQUENCY]
    for note in note1, note2, note3, note4:
        if note:
            freqs.append(get_next_frequency(freqs[-1], note))
    freqs.pop(0)
    while len(freqs) < 4:
        freqs.append(0)
    return freqs