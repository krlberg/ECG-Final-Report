"""Question 5 (manual 2.3.5): cross-correlation between raw sig-P and the filtered sig-F
(high- + low-pass), over the same 5 s window and with the same normalisation as Phase 2.

sig-F is filtered over the whole recording first and then cut to the window, so the filter
run-in of the filters falls outside it.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, load, style
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
# same style as the auto-correlation figure: Phase 2 drawn on top (dashed)
ax.plot(lag, r, color=ECG_COLOR, lw=1.0, label="filtered")
ax.plot(lag, r_raw, color=INK, lw=0.6, ls=(0, (3, 2)), label="unfiltered (Phase 2)")
ax.set_xlim(lag[0], lag[-1])
ax.set_ylim(-0.4, 0.3)
ax.set_xlabel("lag [s]")
ax.set_ylabel(r"normalised $R_{PF}[n]$")
leg = ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=2, fontsize=8, frameon=False,
                borderaxespad=0.2, handlelength=2.0, columnspacing=1.2)
leg.get_lines()[0].set_linewidth(1.5)
fig.savefig(FIG_DIR / "xcorr_filtered.pdf")
plt.close(fig)
