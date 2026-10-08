"""Questions 3a and 4a: auto-correlations of the four signals and the cross-correlation
between sig-P and sig-F, on the 5 s window with the least baseline drift."""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK, INK_2, PLETH_COLOR, load, style

T0, T1 = 36.5, 41.5  # s, 5 s window with the least ECG baseline drift


def corr(x, y):
    """R_xy[n] = sum_m x[m] y[m - n], normalised by sqrt(R_xx[0] R_yy[0]); lags in s."""
    r = np.correlate(x, y, mode="full") / np.sqrt(np.dot(x, x) * np.dot(y, y))
    lag = np.arange(-(len(y) - 1), len(x)) / FS
    return lag, r


style()
t, sig = load()
win = (t >= T0) & (t < T1)
seg = {k: sig[k][win] - sig[k][win].mean() for k in CHANNELS}  # mean removed

for key, (_, name) in CHANNELS.items():
    lag, r = corr(seg[key], seg[key])
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    ax.plot(lag, r, color=PLETH_COLOR if key == "P" else ECG_COLOR, lw=0.6)
    ax.set_xlim(lag[0], lag[-1])
    ax.set_xlabel("lag [s]")
    ax.set_ylabel(r"$R_{xx}[n]/R_{xx}[0]$")
    fig.savefig(FIG_DIR / f"acf_{key}.pdf")
    plt.close(fig)

lag, r = corr(seg["P"], seg["F"])
fig, ax = plt.subplots(figsize=(4.6, 2.2))
ax.plot(lag, r, color=ECG_COLOR, lw=0.6)
ax.set_xlim(lag[0], lag[-1])
ax.set_xlabel("lag [s]")
ax.set_ylabel(r"normalised $R_{PF}$")
# mark the maxima next to zero lag: one beat before and after
for lo, hi, dx, ha in [(-0.5, 0.0, -4, "right"), (0.3, 0.6, 4, "left")]:
    m = (lag > lo) & (lag < hi)
    i = np.flatnonzero(m)[np.argmax(r[m])]
    ax.plot(lag[i], r[i], "o", ms=3, color=INK)
    ax.annotate(f"{lag[i]:+.2f} s".replace("-", "\u2212"), (lag[i], r[i]), xytext=(dx, 4), textcoords="offset points",
                fontsize=7.5, color=INK_2, ha=ha)
    print(f"R_PF max in ({lo}, {hi}) s: {r[i]:.2f} at {lag[i]:.3f} s")
fig.savefig(FIG_DIR / "xcorr_PF.pdf")
plt.close(fig)
