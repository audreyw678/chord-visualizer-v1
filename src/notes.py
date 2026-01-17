import numpy as np
from pyo import *

def get_note(angle):
    if angle:
        bins = np.linspace(45, 150, 8)
        note_index = np.digitize(angle, bins)
        note_index = np.digitize(angle, bins, right=True)
        note_index -= 1
        return max(note_index, 0)


def initiate_pyo():
    s = Server(audio='coreaudio', nchnls=2, duplex=0).boot()
    s.start()

    freqs = [220, 440]
    soft_wave = TriangleTable(order=3)

    osc_list = [Osc(soft_wave, freq=f, mul=0.1) for f in freqs]
    mix = sum(osc_list) / len(osc_list)

    filt_env = Adsr(attack=5, decay=2, sustain=0.7, release=8, dur=0, mul=400)
    lfo = Sine(freq=0.03, mul=150)
    filt = ButLP(mix, freq=800 + filt_env + lfo)

    soft_fuzz = Disto(filt, drive=0.2, slope=0.5)

    amp_env = Adsr(attack=3, decay=1, sustain=0.8, release=6, dur=0, mul=0.6)
    pad = soft_fuzz * amp_env
    amp_env.play()
    filt_env.play()

    chorused = Chorus(pad, depth=1.2, feedback=0.05, bal=0.5)
    rev = Freeverb(chorused, size=0.7, damp=0.6, bal=0.4).out()

    s.gui(locals())

