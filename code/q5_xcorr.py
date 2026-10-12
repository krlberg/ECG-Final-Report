"""Question 5 (manual 2.3.5): cross-correlation between raw sig-P and the filtered sig-F
(high- + low-pass), over the same 5 s window and with the same normalisation as Phase 2.

sig-F is filtered over the whole recording first and then cut to the window, so the filter
start-up transients fall outside it. Both filters have zero phase, so the lags are not shifted.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, INK_2, load, style
from filters import filtered_F

T0, T1 = 36.5, 41.5  # s, same window as Phase 2


def corr(x, y):
    """R_xy[n] = sum_m x[m] y[m - n], normalised by sqrt(R_xx[0] R_yy[0]); lags in s."""
    r = np.correlate(x, y, mode="full") / np.sqrt(np.dot(x, x) * np.dot(y, y))
    lag = np.arange(-(len(y) - 1), len(x)) / FS
    return lag, r


def maxima(lag, r, lim=2.5):
    """Local maxima above 0 within |lag| < lim (at least 0.4 s apart)."""
    i, _ = ss.find_peaks(r, distance=int(0.4 * FS))
    return i[(np.abs(lag[i]) < lim) & (r[i] > 0)]


style()
t, sig = load()
_, raw, _, filt = filtered_F()
win = (t >= T0) & (t < T1)
P = sig["P"][win] - sig["P"][win].mean()  # raw sig-P, mean removed
F = {"filt": filt[win] - filt[win].mean(), "raw": raw[win] - raw[win].mean()}

lag, r = corr(P, F["filt"])
_, r_raw = corr(P, F["raw"])
_, a = corr(F["filt"], F["filt"])  # ACF of filtered sig-F, for 5c

print(f"energy of filtered / raw sig-F in window: {np.dot(F['filt'], F['filt']) / np.dot(F['raw'], F['raw']):.3f}")
for name, y in [("R_PF filtered", r), ("R_PF raw (Phase 2)", r_raw)]:
    i = maxima(lag, y)
    print(name + ":", ", ".join(f"{y[k]:.3f} at {lag[k]:+.3f} s" for k in i))
    print(f"  spacing of maxima: {np.round(np.diff(lag[i]), 3)} s;  minimum {y.min():.3f} at {lag[np.argmin(y)]:+.3f} s")
i = maxima(lag, a, lim=3.0)
i = i[lag[i] >= 0]
print("ACF filtered sig-F:", ", ".join(f"{a[k]:.3f} at {lag[k]:.3f} s" for k in i))
print(f"  mean period: {np.mean(np.diff(lag[i])):.3f} s")

fig, ax = plt.subplots(figsize=(4.2, 2.4))
ax.plot(lag, r_raw, color=INK_2, lw=0.6, ls="--", alpha=0.6, label="raw sig-F (Phase 2)")
ax.plot(lag, r, color=ECG_COLOR, lw=0.7, label="filtered sig-F")
ax.set_xlim(lag[0], lag[-1])
ax.set_ylim(-0.3, 0.3)
ax.set_xlabel("lag [s]")
ax.set_ylabel(r"normalised $R_{PF}$")
# mark the maxima next to zero lag: one beat before and after
for lo, hi, dx, ha in [(-0.5, 0.0, -4, "right"), (0.3, 0.6, 4, "left")]:
    m = (lag > lo) & (lag < hi)
    i = np.flatnonzero(m)[np.argmax(r[m])]
    ax.plot(lag[i], r[i], "o", ms=3, color=INK)
    ax.annotate(f"{r[i]:.2f} at {lag[i]:+.2f} s".replace("-", "−"), (lag[i], r[i]), xytext=(dx, 4),
                textcoords="offset points", fontsize=7.5, color=INK_2, ha=ha)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=7.5, frameon=False, ncol=2)
fig.savefig(FIG_DIR / "xcorr_filtered.pdf")
plt.close(fig)
