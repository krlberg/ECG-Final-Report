"""Question 4a-b: auto-correlation of the filtered sig-F (high- + low-pass), compared with
the unfiltered sig-F of Phase 2. Same 5 s window, mean removal and normalisation as Phase 2
(intermediate-report, q3a_q4a_corr.py). The filters run on the whole recording, so the
window is free of the filter run-in."""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, style
from filters import filtered_F

T0, T1 = 36.5, 41.5  # s, same window as Phase 2


def corr(x, y):
    """R_xy[n] = sum_m x[m] y[m - n], normalised by sqrt(R_xx[0] R_yy[0]); lags in s."""
    r = np.correlate(x, y, mode="full") / np.sqrt(np.dot(x, x) * np.dot(y, y))
    lag = np.arange(-(len(y) - 1), len(x)) / FS
    return lag, r


style()
t, raw, _, filt = filtered_F()
win = (t >= T0) & (t < T1)
acf, power = {}, {}
for name, x in [("unfiltered", raw), ("filtered", filt)]:
    seg = x[win] - x[win].mean()  # mean removed
    lag, r = corr(seg, seg)
    acf[name], power[name] = r, np.mean(seg**2)

    pos = lag > 0
    pk, _ = ss.find_peaks(r[pos], height=0.2, distance=int(0.4 * FS))  # beat peaks
    beat = (lag > 0) & (lag < 0.72)
    i = np.argmin(r[beat])
    period = np.mean(np.diff(np.r_[0.0, lag[pos][pk]]))
    print(f"{name}: side peaks {np.round(r[pos][pk], 2)} at {np.round(lag[pos][pk], 3)} s; "
          f"deepest dip {r[beat][i]:.2f} at {lag[beat][i]:.3f} s; "
          f"mean period {period:.3f} s -> {60 / period:.0f} bpm")

# power removed by the filters lowers R_xx[0]; it does not repeat every beat
ratio = power["filtered"] / power["unfiltered"]
print(f"power filtered/unfiltered: {ratio:.3f}; unfiltered first side peak / ratio: "
      f"{acf['unfiltered'][np.argmin(abs(lag - 0.72))] / ratio:.2f}")

fig, (ax, az) = plt.subplots(1, 2, figsize=(6.4, 2.4), gridspec_kw={"width_ratios": [1.6, 1]})
# R_xx is symmetric, so only positive delays are shown; Phase 2 drawn on top (dashed) so the difference stays visible
for a in (ax, az):
    a.plot(lag, acf["filtered"], color=ECG_COLOR, lw=1.0, label="filtered")
    a.plot(lag, acf["unfiltered"], color=INK, lw=0.6, ls=(0, (3, 2)), label="unfiltered (Phase 2)")
    a.set_xlabel("delay [s]")
ax.set_xlim(0, 5.0)
ax.set_ylabel(r"$R_{x,x}[n]/R_{x,x}[0]$")
# zoom on the first period: dot on the values quoted in 4b (dip next to zero delay, first side peak)
az.set_xlim(0, 0.9)
az.set_ylim(-0.3, 1.02)
az.set_title("zoom, 0–0.9 s", fontsize=8)
for name, c in [("filtered", ECG_COLOR), ("unfiltered", INK)]:
    r = acf[name]
    d = (lag > 0) & (lag < 0.3)
    i = np.flatnonzero(d)[np.argmin(r[d])]
    k = np.flatnonzero((lag > 0.6) & (lag < 0.85))
    k = k[np.argmax(r[k])]
    f = name == "filtered"
    for j, xy in [(i, (7, -9) if f else (7, 1)), (k, (6, 2) if f else (-6, 2))]:
        az.plot(lag[j], r[j], "o", color=c, ms=3)
        az.annotate(f"{r[j]:.2f}", (lag[j], r[j]), xytext=xy, textcoords="offset points",
                    fontsize=7, color=c, ha="left" if xy[0] > 0 else "right")
leg = ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=2, fontsize=8, frameon=False,
                borderaxespad=0.2, handlelength=2.0, columnspacing=1.2)
leg.get_lines()[0].set_linewidth(1.5)
fig.tight_layout()
fig.savefig(FIG_DIR / "acf_filtered.pdf")
plt.close(fig)
