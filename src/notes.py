import numpy as np

def get_note(angle):
    if angle:
        bins = np.linspace(45, 130, 8)
        note_index = np.digitize(angle, bins)
        note_index = np.digitize(angle, bins, right=True)
        note_index -= 1
        return max(note_index, 0)
