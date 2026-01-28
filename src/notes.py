import numpy as np
from config import *


def get_chord_type(finger_states, hand_spread):
    """Chord mappings:
    Major chord: all fingers up, spread out
    Minor chord: all fingers up, close together
    Diminished 7 chord: index finger up
    Minor 7 chord: index and middle fingers up
    Dominant 7 chord: index, middle, and ring fingers up
    Major 7 chord: index, middle, ring, pinky fingers up
    Sus2 chord: thumb and index fingers up
    Sus4 chord: thumb and pinky fingers up
    Sus24 chord: thumb, index, pinky fingers up"""
    if finger_states == [True, True, True, True, True]:
        if hand_spread:
            return "Major"
        else:
            return "Minor"
    elif finger_states == [False, True, False, False, False]:
        return "Diminished7"
    elif finger_states == [False, True, True, False, False]:    
        return "Minor7"
    elif finger_states == [False, True, True, True, False]:
        return "Dominant7"
    elif finger_states == [False, True, True, True, True]:
        return "Major7"
    elif finger_states == [True, True, False, False, False]:
        return "Sus2"
    elif finger_states == [True, False, False, False, True]:
        return "Sus4"
    elif finger_states == [True, True, False, False, True]:
        return "Sus24"

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
    if triangle_area is None:
        return 0.0
    volume = triangle_area / max_area
    volume = min(max(volume, min_area), 1)
    return volume