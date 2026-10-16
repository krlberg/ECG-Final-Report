"""Question 2a: single-sided amplitude spectra of the four raw signals, 0-80 Hz."""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK, INK_2, PLETH_COLOR, load, style

F_MAX = 80.0  # Hz, range asked for in the manual
T0, T1 = 35.0, 45.0  # s, same 10 s window as question 1a

style()
t, sig = load()
win = (t >= T0) & (t < T1)
seg = {k: sig[k][win] for k in CHANNELS}
N = int(win.sum())
f = np.arange(N // 2 + 1) * FS / N  # f_k = k fs / N, resolution fs/N = 0.1 Hz

# heart-rate fundamental: the pleth has the clearest peak
x_p = seg["P"] - seg["P"].mean()
A_p = 2 * np.abs(np.fft.rfft(x_p)) / N
f_hr = f[np.argmax(A_p * ((f > 1.0) & (f < 2.0)))]

for key, (_, name) in CHANNELS.items():
    x = seg[key] - seg[key].mean()  # only changes X[0]
    X = np.fft.rfft(x)  # X[k] = sum x[n] exp(-j 2 pi k n / N), k = 0..N/2
    A = 2 * np.abs(X) / N  # single-sided amplitude: a sinusoid of amplitude A gives a peak A
    keep = (f > 0) & (f <= F_MAX)

    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    color = PLETH_COLOR if key == "P" else ECG_COLOR
    ax.semilogy(f[keep], A[keep], color=color, lw=0.4)
    ax.set_xlim(0, F_MAX)
    ax.set_xlabel("f [Hz]")
    unit = "a.u." if key == "P" else r"$\mu$V"
    ax.set_ylabel(f"$2|X[k]|/N$ [{unit}]")

    # mark the heart-rate fundamental and, for the ECG, the mains line
    k_hr = np.argmin(np.abs(f - f_hr))
    ax.plot(f[k_hr], A[k_hr], "o", ms=2.5, color=INK, zorder=3)
    ax.annotate(rf"$f_\mathrm{{HR}}$ = {f_hr:.2f} Hz", (f[k_hr], A[k_hr]), xytext=(18, 4),
                textcoords="offset points", fontsize=7.5, color=INK_2, va="center",
                arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.6, shrinkA=1, shrinkB=3))
    if key != "P":
        k50 = np.argmax(A * ((f > 49.5) & (f < 50.5)))
        ax.plot(f[k50], A[k50], "o", ms=2.5, color=INK, zorder=3)
        ax.annotate("50 Hz", (f[k50], A[k50]), xytext=(0, 12), textcoords="offset points",
                    fontsize=7.5, color=INK_2, ha="center",
                    arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.6, shrinkA=1, shrinkB=3))

    fig.savefig(FIG_DIR / f"fft_{key}.pdf")
    plt.close(fig)
