"""Checks behind the explanations in 1a, 5b and 5c (prints only, no figures).

1a: sig-P has almost no power between 7 and 40 Hz, so the upper band edge does not affect its SNR.
5b: the xcorr maxima are 0.67 s apart instead of one period, because the pulse wave also lines up
    with the T wave; without the T-wave region of sig-F they lie about one period apart.
5c: timing of the pulse wave after the R peak (minimum, maximum), averaged over the window.
"""
import numpy as np
import scipy.signal as ss

from ecg_data import FS, load
from filters import filtered_F
from q1a_snr import power_spectrum, snr_db

T0, T1 = 36.5, 41.5  # s, same window as Q4/Q5

t, sig = load()
_, _, _, filt = filtered_F()

# 1a
f, P = power_spectrum(sig["P"])
print(f"sig-P: power 7-40 Hz = {100 * P[(f > 7) & (f <= 40)].sum() / P.sum():.2f}%, "
      f"SNR 0.5-40 Hz = {snr_db(f, P):.1f} dB, 0.5-10 Hz = {snr_db(f, P, (0.5, 10)):.1f} dB")

# R peaks of the filtered sig-F
pk, _ = ss.find_peaks(filt, height=0.5 * np.percentile(filt, 99.9), distance=int(0.4 * FS))
win = (t >= T0) & (t < T1)
Pw = sig["P"][win] - sig["P"][win].mean()
lag = np.arange(-(win.sum() - 1), win.sum()) / FS


def maxima(x):
    """Normalised R_PF maxima near -0.25 and +0.42 s for a version x of sig-F."""
    F = x[win] - x[win].mean()
    r = np.correlate(Pw, F, "full") / np.sqrt(np.dot(Pw, Pw) * np.dot(F, F))
    out = []
    for L in (-0.25, 0.42):
        i = np.argmin(np.abs(lag - L))
        j = slice(i - 200, i + 200)
        out.append(f"{r[j].max():.3f} at {lag[j][np.argmax(r[j])]:+.3f} s")
    return ", ".join(out)


# 5b: remove the T-wave region (0.10-0.45 s after each R peak)
mask = np.ones_like(filt)
for k in pk:
    mask[k + int(0.10 * FS):k + int(0.45 * FS)] = 0
print("R_PF maxima, filtered sig-F:   ", maxima(filt))
print("R_PF maxima, without T wave:   ", maxima(filt * mask))

# 5c: average pulse wave after the R peaks in the window
L = int(0.7 * FS)
pw = [k for k in pk if T0 <= t[k] < T1 and k + L < len(t)]
avg = np.mean([sig["P"][k:k + L] for k in pw], axis=0)
print(f"pulse wave after R peak ({len(pw)} beats): minimum at {np.argmin(avg) / FS:.3f} s, "
      f"maximum at {np.argmax(avg) / FS:.3f} s")
