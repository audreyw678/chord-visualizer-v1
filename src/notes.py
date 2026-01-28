import numpy as np
from config import *

MAJOR_CHORD = [0, 4, 7, 12]
MINOR_CHORD = [0, 3, 7, 12]
DIMINISHED7_CHORD = [0, 3, 6, 9, 12]
MINOR7_CHORD = [0, 3, 7, 10, 12]
DOMINANT7_CHORD = [0, 4, 7, 10, 12]
MAJOR7_CHORD = [0, 4, 7, 11, 12]
SUS2_CHORD = [0, 2, 7, 12]
SUS4_CHORD = [0, 5, 7, 12]
SUS24_CHORD = [0, 2, 5, 7, 12]

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
            return MAJOR_CHORD
        else:
            return MINOR_CHORD
    elif finger_states == [False, True, False, False, False]:
        return DIMINISHED7_CHORD
    elif finger_states[1:] == [True, True, False, False]:
        return MINOR7_CHORD
    elif finger_states[1:] == [True, True, True, False]:
        return DOMINANT7_CHORD
    elif finger_states[1:] == [True, True, True, True]:
        return MAJOR7_CHORD
    elif finger_states == [True, True, False, False, False]:
        return SUS2_CHORD
    elif finger_states == [True, False, False, False, True]:
        return SUS4_CHORD
    elif finger_states == [True, True, False, False, True]:
        return SUS24_CHORD
    else:
        return None

def get_chord_freqs(chord_notes, root_note=BASE_FREQUENCY):
    if chord_notes is None:
        return [None for i in range(MAX_CHORD_NOTES)]
    frequencies = [None for i in range(MAX_CHORD_NOTES)]
    for i, note in enumerate(chord_notes):
        if note is not None:
            freq = root_note * (2 ** (note / 12))
            frequencies[i] = freq
        else:
            frequencies[i] = None
    return frequencies

def get_volume_as_float(triangle_area, max_area=0.005, min_area=0.0002):
    if triangle_area is None:
        return 0.0
    volume = triangle_area / max_area
    volume = min(max(volume, min_area), 1)
    return volume