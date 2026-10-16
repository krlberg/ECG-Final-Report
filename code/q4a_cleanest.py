"""Question 4a: which ECG channel is cleanest.

Ratio = mean QRS peak-to-peak amplitude / mean noise std between beats, over the 5 s
correlation window. Noise is taken 0.50-0.60 s after each R-peak (after the T wave, before
the next P wave), with a straight line removed to exclude drift.
"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from ecg_data import FS, load

T0, T1 = 36.5, 41.5

t, sig = load()

# R-peaks from sig-F (largest positive QRS): local maxima of the drift-removed signal
k = int(FS)
y = sig["F"] - np.convolve(sig["F"], np.ones(k) / k, mode="same")
y[:k] = y[-k:] = 0
h = int(0.25 * FS)
local_max = np.pad(sliding_window_view(y, 2 * h + 1).max(axis=1), (h, h))
peaks = np.flatnonzero((y == local_max) & (y > 0.5 * np.percentile(y, 99.8)))
peaks = peaks[(t[peaks] > T0) & (t[peaks] < T1 - 0.7)]

n = np.arange(int(0.5 * FS), int(0.6 * FS))
for key in "RLF":
    x = sig[key]
    qrs = np.mean([np.ptp(x[p - 40:p + 40]) for p in peaks])
    noise = np.mean([np.std(x[p + n] - np.polyval(np.polyfit(n, x[p + n], 1), n)) for p in peaks])
    print(f"sig-{key}: QRS {qrs:.0f} uV, noise {noise:.1f} uV, ratio {qrs / noise:.0f}")
