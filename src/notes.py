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
node_idx_to_semitones = [0, 2, 4, 5, 7, 9, 11, 12]

# Formula for calculating 12-TET frequencies:
# P_{n} = P_{a} * 2^(n/12), where P_{a} is a reference frequency (like A4=440 Hz), 
# n is the number of semitones from that reference, and 2^(1/12)
# is the constant multiplier for each half-step, dividing the octave into 12 equal logarithmic steps. 
def get_next_frequency(prev_freq, next_note_number):
    global node_idx_to_semitones
    num_semitones = node_idx_to_semitones[next_note_number]
    next_freq = prev_freq * 2 ** (num_semitones/12)
    # shift node_idx list
    if next_note_number != 0:
        node_idx_to_semitones = node_idx_to_semitones[next_note_number:] + [12 + i for i in node_idx_to_semitones[1:next_note_number]]
        node_idx_to_semitones = [i - node_idx_to_semitones[0] for i in node_idx_to_semitones]
        node_idx_to_semitones.append(node_idx_to_semitones[0]+12)
    return next_freq

def reset_note_mapping():
    global node_idx_to_semitones
    node_idx_to_semitones = [0, 2, 4, 5, 7, 9, 11, 12]

def get_chord_freqs(note1, note2, note3, note4):
    freqs = [BASE_FREQUENCY]
    for note in note1, note2, note3, note4:
        if note != None:
            freqs.append(get_next_frequency(freqs[-1], note))
    freqs.pop(0)
    while len(freqs) < 4:
        freqs.append(0)
    return freqs

def get_volume_as_float(triangle_area, max_area=0.005, min_area=0.0002):
    volume = triangle_area / max_area
    volume = min(max(volume, min_area), 1)
    return volume