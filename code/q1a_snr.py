"""Question 1a (manual 2.3.1a): SNR of the four raw signals over the whole recording.

Power per DFT bin (one-sided): P[k] = 2|X[k]|^2 / N^2, so sum_k P[k] = mean power (Parseval).
Power inside the band B_s is signal, all other power is noise.
"""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK_2, load, style

BAND = (0.5, 40.0)  # Hz, signal band: above most drift, below the 50 Hz mains
NOISE_COLOR = "#a3a29e"  # grey


def power_spectrum(x):
    """One-sided power per bin, mean removed."""
    x = x - x.mean()
    N = len(x)
    P = 2 * np.abs(np.fft.rfft(x)) ** 2 / N**2
    P[0] = 0.0
    return np.fft.rfftfreq(N, 1 / FS), P


def band_powers(f, P, band=BAND):
    inside = (f >= band[0]) & (f <= band[1])
    return P[inside].sum(), P[~inside].sum()


def snr_db(f, P, band=BAND):
    P_s, P_n = band_powers(f, P, band)
    return 10 * np.log10(P_s / P_n)


def sci(v):
    e = int(np.floor(np.log10(v)))
    return rf"{v / 10**e:.2f}$\cdot 10^{{{e}}}$"


if __name__ == "__main__":
    style()
    t, sig = load()
    for key, (_, name) in CHANNELS.items():
        print(f"{name}: SNR = {snr_db(*power_spectrum(sig[key])):.1f} dB")

    # window-length dependence (points to pay attention to)
    for t0 in (0, 10, 20, 30):
        win = (t >= t0) & (t < t0 + 10)
        print(f"sig-F, {t0}-{t0 + 10} s: SNR = {snr_db(*power_spectrum(sig['F'][win])):.1f} dB")

    # method figure: all four signals, signal bins (inside B_s) blue, noise bins grey
    lo, hi = BAND
    fig, axes = plt.subplots(2, 2, figsize=(6.3, 4.6), sharex=True, layout="constrained")
    for ax, (key, (_, name)) in zip(axes.flat, CHANNELS.items()):
        f, P = power_spectrum(sig[key])
        P_s, P_n = band_powers(f, P)
        unit = "a.u.$^2$" if key == "P" else r"$\mu$V$^2$"
        inside = (f >= lo) & (f <= hi)
        out = np.where(inside, np.nan, P)  # noise bins (outside B_s)
        out[np.flatnonzero(inside)[[0, -1]] + [-1, 1]] = P[np.flatnonzero(inside)[[0, -1]] + [-1, 1]]
        ax.loglog(f[1:], out[1:], color=NOISE_COLOR, lw=0.4)
        ax.loglog(f[inside], P[inside], color=ECG_COLOR, lw=0.4)
        for edge in BAND:  # band edges of B_s
            ax.axvline(edge, color=INK_2, lw=0.6, ls=(0, (3, 2)), zorder=1)
        ax.set_xlim(f[1], FS / 2)
        snr = f"{10 * np.log10(P_s / P_n):.1f}".replace("-", "\u2212")
        ax.set_title(f"{name}: SNR = {snr} dB", fontsize=9, loc="left")
        ax.text(0.03, 0.17, f"signal {sci(P_s)}", transform=ax.transAxes, ha="left", va="bottom",
                fontsize=7, color=ECG_COLOR, bbox=dict(fc="white", ec="none", pad=0.5))
        ax.text(0.03, 0.05, f"noise {sci(P_n)}", transform=ax.transAxes, ha="left", va="bottom",
                fontsize=7, color=INK_2, bbox=dict(fc="white", ec="none", pad=0.5))
        if ax in axes[1]:
            ax.set_xlabel("f [Hz]")
        ax.set_ylabel(f"$P[k]$ [{unit}]")
    fig.savefig(FIG_DIR / "snr_all.pdf")
    plt.close(fig)
