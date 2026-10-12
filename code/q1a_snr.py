"""Question 1a (manual 2.3.1a): SNR of the four raw signals over the whole recording.

Power per DFT bin (one-sided): P[k] = 2|X[k]|^2 / N^2, so sum_k P[k] = mean power (Parseval).
Power inside the heartbeat band is signal, all other power is noise.
"""
import matplotlib.pyplot as plt
import numpy as np

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, FS, INK_2, load, style

# heartbeat (signal) band in Hz
BAND = {"P": (0.5, 10.0), "R": (0.5, 40.0), "L": (0.5, 40.0), "F": (0.5, 40.0)}


def power_spectrum(x):
    """One-sided power per bin, mean removed."""
    x = x - x.mean()
    N = len(x)
    P = 2 * np.abs(np.fft.rfft(x)) ** 2 / N**2
    P[0] = 0.0
    return np.fft.rfftfreq(N, 1 / FS), P


def snr_db(f, P, band):
    inside = (f >= band[0]) & (f <= band[1])
    return 10 * np.log10(P[inside].sum() / P[~inside].sum())


if __name__ == "__main__":
    style()
    t, sig = load()
    for key, (_, name) in CHANNELS.items():
        f, P = power_spectrum(sig[key])
        print(f"{name}: SNR = {snr_db(f, P, BAND[key]):.1f} dB")

    # method figure for sig-F
    f, P = power_spectrum(sig["F"])
    lo, hi = BAND["F"]
    fig, ax = plt.subplots(figsize=(4.2, 2.4))
    ax.axvspan(lo, hi, color=ECG_COLOR, alpha=0.12, lw=0)
    ax.loglog(f[1:], P[1:], color=ECG_COLOR, lw=0.4)
    ax.set_xlim(f[1], FS / 2)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$P[k]$ [$\mu$V$^2$]")
    top = ax.get_ylim()[1]
    for x, label in [(np.sqrt(lo * hi), "signal"), (0.1, "noise"), (150, "noise")]:
        ax.text(x, top, label, ha="center", va="top", fontsize=8, color=INK_2)
    fig.savefig(FIG_DIR / "snr_F.pdf")
    plt.close(fig)
