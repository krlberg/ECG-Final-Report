"""Question 1a (manual 2.3.1a): SNR of the four raw signals, following Learning Task 3.

Power per DFT bin (one-sided): P[k] = 2|X[k]|^2 / N^2, so sum_k P[k] = mean power (Parseval).
Signal band B_s holds the heartbeat; a signal-free band B_n just above it gives the noise floor
density rho, extrapolated into B_s.  P_s = P(B_s) - rho*|B_s|, P_n = P_total - P_s.
"""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK, INK_2, PLETH_COLOR, load, style

T0, T1 = 35.0, 45.0  # s, same 10 s window as Phase 2

# (signal band, noise-floor band) in Hz
BANDS = {
    "P": ((0.5, 10.0), (15.0, 35.0)),
    "R": ((0.5, 40.0), (60.0, 90.0)),
    "L": ((0.5, 40.0), (60.0, 90.0)),
    "F": ((0.5, 40.0), (60.0, 90.0)),
}


def power_spectrum(x):
    """One-sided power per bin, mean removed (DC is neither signal nor noise)."""
    x = x - x.mean()
    N = len(x)
    P = 2 * np.abs(np.fft.rfft(x)) ** 2 / N**2
    P[0] = 0.0
    return np.fft.rfftfreq(N, 1 / FS), P


def snr(f, P, bands):
    """Return P_s, P_n, rho for one signal."""
    (s1, s2), (n1, n2) = bands
    rho = P[(f >= n1) & (f <= n2)].sum() / (n2 - n1)  # noise power per Hz
    P_s = P[(f >= s1) & (f <= s2)].sum() - rho * (s2 - s1)
    P_n = P.sum() - P_s
    return P_s, P_n, rho


def plot_method(key, f, P, bands, rho):
    (s1, s2), (n1, n2) = bands
    df = f[1] - f[0]
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    color = PLETH_COLOR if key == "P" else ECG_COLOR
    ax.axvspan(s1, s2, color=color, alpha=0.12, lw=0)
    ax.axvspan(n1, n2, color=INK_2, alpha=0.15, lw=0)
    ax.loglog(f[1:], P[1:], color=color, lw=0.4)
    ax.hlines(rho * df, s1, n2, color=INK, lw=0.8, ls="--")  # floor level per bin
    ax.text(s1 * 1.15, rho * df, r"$\rho\,\Delta f$", ha="left", va="bottom", fontsize=7.5, color=INK)
    ax.set_xlim(0.1, FS / 2)
    ax.set_xlabel("f [Hz]")
    unit = "a.u.$^2$" if key == "P" else r"$\mu$V$^2$"
    ax.set_ylabel(f"$P[k]$ [{unit}]")
    top = ax.get_ylim()[1]
    ax.text(np.sqrt(s1 * s2), top, "signal", ha="center", va="top", fontsize=7, color=INK_2)
    ax.text(np.sqrt(n1 * n2), top, "noise\nfloor", ha="center", va="top", fontsize=7, color=INK_2)
    ax.text(0.2, top, "drift", ha="center", va="top", fontsize=7, color=INK_2)
    fig.savefig(FIG_DIR / f"snr_{key}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    style()
    t, sig = load()
    win = (t >= T0) & (t < T1)
    print(f"{'signal':8}{'P_s':>12}{'P_n':>12}{'SNR':>8}{'SNR [dB]':>10}")
    for key, (_, name) in CHANNELS.items():
        f, P = power_spectrum(sig[key][win])
        P_s, P_n, rho = snr(f, P, BANDS[key])
        print(f"{name:8}{P_s:12.4g}{P_n:12.4g}{P_s / P_n:8.2f}{10 * np.log10(P_s / P_n):10.1f}")
        if key in ("P", "F"):
            plot_method(key, f, P, BANDS[key], rho)
