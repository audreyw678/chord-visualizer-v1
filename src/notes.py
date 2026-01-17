import numpy as np

# C: 90.00° to 102.86°
# D: 102.86° to 115.71°
# E: 115.71° to 128.57°
# F: 128.57° to 141.43°
# G: 141.43° to 154.29°
# A: 154.29° to 167.14°
# B: 167.14° to 180.00°

def get_note(angle):
    if angle:
        bins = np.linspace(45, 130, 8)
        note_index = np.digitize(angle, bins)
        note_index = np.digitize(angle, bins, right=True)
        note_index -= 1
        return max(note_index, 0)
