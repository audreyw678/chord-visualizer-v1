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

    freqs = [440, 554.37, 659.26, 830.6]  # you can add more notes
    osc_list = []
    soft_saw = TriangleTable(order=3) # can also do TriangleTable
    osc_list = []
    for f in freqs:
        drift = Randi(min=0.9995, max=1.0005, freq=0.02)
        osc_list.append(Osc(soft_saw, freq=f * drift, mul=0.1))

    mix = sum(osc_list) / len(osc_list)
    filt_env = Adsr(attack=5, decay=2, sustain=0.7, release=8, dur=0, mul=400)
    filt = ButLP(mix, freq=1000)
    soft_fuzz = Disto(filt, drive=0.3, slope=0.5)
    amp_env = Adsr(
        attack=3,
        decay=1,
        sustain=0.8,
        release=6,
        dur=0,
        mul=0.6
    )
    pad = filt * amp_env
    amp_env.play()
    filt_env.play()
    lfo = Sine(freq=0.03, mul=150)  # slow, subtle sweep
    filt.freq = 800 + filt_env + lfo
    chorused = Chorus(
        pad,
        depth=1.95,
        feedback=0,
        bal=0.5
    )
    rev = Freeverb(
        chorused,
        size=0.85,
        damp=0.6,
        bal=0.4
    ).out()
    s.gui(locals())