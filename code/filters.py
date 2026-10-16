"""High-pass (Q2) and low-pass (Q3) filters for sig-F, shared by questions 2-5.

HP: linear-phase FIR, window method (Hamming), K = 4097 taps, f_c = 0.5 Hz (-6 dB).
    Chosen over an IIR filter: the IIR phase shifts the slow ECG parts (60 ms at f_HR for a
    2nd-order Butterworth) and with it the pulse delay in Q5. Applied to the mean-removed
    signal as a centred convolution, which removes its delay of (K-1)/2 = 2048 samples.
LP: linear-phase FIR, window method (Hamming), K = 201 taps, f_c = 40 Hz (-6 dB).
    Applied as a centred convolution, which removes its delay of (K-1)/2 = 100 samples.
"""
import numpy as np
import scipy.signal as ss

from ecg_data import FS, load

HP_K, HP_FC = 4097, 0.5  # taps, Hz
LP_K, LP_FC = 201, 40.0  # taps, Hz

HP_H = ss.firwin(HP_K, HP_FC, pass_zero=False, window="hamming", fs=FS)  # h[n], symmetric
LP_H = ss.firwin(LP_K, LP_FC, window="hamming", fs=FS)  # h[n], symmetric


def highpass(x):
    # mean removed first, so the DC offset does not enter the run-in at the edges
    return np.convolve(x - x.mean(), HP_H, mode="same")


def lowpass(x):
    return np.convolve(x, LP_H, mode="same")


def filtered_F():
    """Return t and sig-F raw, high-pass filtered, and high- + low-pass filtered."""
    t, sig = load()
    raw = sig["F"]
    hp = highpass(raw)
    return t, raw, hp, lowpass(hp)
