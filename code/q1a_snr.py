"""Question 1a (manual 2.3.1a): SNR of the four raw signals over the whole recording.

Power per DFT bin (one-sided): P[k] = 2|X[k]|^2 / N^2, so sum_k P[k] = mean power (Parseval).
Power inside the band B_s is signal, all other power is noise.
"""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK_2, load, style

BAND = (0.5, 40.0)  # Hz, signal band: above most drift, below the 50 Hz mains


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

    # method figure for sig-F
    f, P = power_spectrum(sig["F"])
    P_s, P_n = band_powers(f, P)
    lo, hi = BAND
    fig, ax = plt.subplots(figsize=(4.2, 2.4))
    ax.axvspan(lo, hi, color=ECG_COLOR, alpha=0.12, lw=0)
    ax.loglog(f[1:], P[1:], color=ECG_COLOR, lw=0.4)
    ax.set_xlim(f[1], FS / 2)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$P[k]$ [$\mu$V$^2$]")
    ax.text(np.sqrt(lo * hi), 0.98, f"signal\n{sci(P_s)} $\\mu$V$^2$", transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=7.5, color=INK_2)
    ax.text(0.03, 0.06, f"noise\n{sci(P_n)} $\\mu$V$^2$", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=7.5, color=INK_2)
    fig.savefig(FIG_DIR / "snr_F.pdf")
    plt.close(fig)
