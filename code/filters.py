"""High-pass (Q2) and low-pass (Q3) filters for sig-F, shared by questions 2-5.

HP: IIR Butterworth, order 2, f_c = 0.5 Hz, applied forward and backward (zero phase).
    An FIR with a 0.5 Hz edge would need K ~ f_s / 0.5 Hz > 2000 taps.
LP: linear-phase FIR, window method (Hamming), K = 201 taps, f_c = 40 Hz (-6 dB).
    Applied as a centred convolution, which removes its delay of (K-1)/2 = 100 samples.
"""
import numpy as np
import scipy.signal as ss

from ecg_data import FS, load

HP_ORDER, HP_FC = 2, 0.5  # Hz
LP_K, LP_FC = 201, 40.0  # taps, Hz

HP_SOS = ss.butter(HP_ORDER, HP_FC, "highpass", fs=FS, output="sos")
LP_H = ss.firwin(LP_K, LP_FC, window="hamming", fs=FS)  # h[n], symmetric


def highpass(x):
    return ss.sosfiltfilt(HP_SOS, x)


def lowpass(x):
    return np.convolve(x, LP_H, mode="same")


def filtered_F():
    """Return t and sig-F raw, high-pass filtered, and high- + low-pass filtered."""
    t, sig = load()
    raw = sig["F"]
    hp = highpass(raw)
    return t, raw, hp, lowpass(hp)
