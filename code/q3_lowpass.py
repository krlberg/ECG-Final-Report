"""Question 3 (manual 2.3.3): low-pass FIR filter (design in filters.py) applied to high-pass filtered sig-F.

Figures: magnitude response of the FIR, and raw / high-pass / high- + low-pass sig-F in time and frequency.
Prints the SNR of the three signals (same band and whole recording as question 1a).
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, INK_2, style
from filters import LP_FC, LP_H, filtered_F
from q1a_snr import power_spectrum, snr_db

T0, T1 = 38.0, 40.5  # s, three beats inside the clean 35-45 s stretch
RAW_COLOR = "#a3a29e"  # grey: raw signal
HP_COLOR = "#9cc2ee"  # light blue: high-pass only


def mark(ax, f0, dB, text, xytext):
    ax.plot(f0, dB, "o", ms=2.5, color=INK, zorder=3)
    ax.annotate(text, (f0, dB), xytext=xytext, textcoords="offset points", fontsize=7.5, color=INK_2,
                va="center", arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.6, shrinkA=1, shrinkB=3))


if __name__ == "__main__":
    style()
    t, raw, hp, lp = filtered_F()
    for name, z in (("raw", raw), ("high-pass", hp), ("high- + low-pass", lp)):
        print(f"sig-F {name}: SNR = {snr_db(*power_spectrum(z)):.1f} dB")

    # magnitude response 20 log10 |H(f)|
    f, H = ss.freqz(LP_H, worN=2**15, fs=FS)
    H_dB = 20 * np.log10(np.abs(H))
    at = lambda f0: H_dB[np.argmin(np.abs(f - f0))]
    print(f"|H| at 35 Hz: {at(35):.1f} dB, 40 Hz: {at(40):.1f} dB, 50 Hz: {at(50):.1f} dB, "
          f"100 Hz: {at(100):.1f} dB")

    fig, ax = plt.subplots(figsize=(4.2, 2.4))
    ax.axvspan(0, 32, color=ECG_COLOR, alpha=0.12, lw=0)
    ax.plot(f, H_dB, color=ECG_COLOR, lw=0.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(-80, 5)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$20\log_{10}|H(f)|$ [dB]")
    ax.text(16, -40, "pass band\n(ECG content)", ha="center", va="center", fontsize=7.5, color=INK_2)
    mark(ax, LP_FC, at(LP_FC), rf"$f_c$ = {LP_FC:.0f} Hz (${at(LP_FC):.0f}$ dB)", (12, 6))
    mark(ax, 50, at(50), f"50 Hz mains: ${at(50):.1f}$ dB", (14, 12))
    fig.savefig(FIG_DIR / "lp_response.pdf")
    plt.close(fig)

    # time domain: short stretch; raw with its window mean removed (large DC offset)
    win = (t >= T0) & (t < T1)
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    ax.plot(t[win], raw[win] - raw[win].mean(), color=RAW_COLOR, lw=0.6, label="raw")
    ax.plot(t[win], hp[win], color=HP_COLOR, lw=0.6, label="HP")
    ax.plot(t[win], lp[win], color=ECG_COLOR, lw=0.8, label="HP + LP")
    ax.set_xlim(T0, T1)
    ax.set_xlabel("t [s]")
    ax.set_ylim(-300, 1000)  # headroom for the legend
    ax.set_ylabel(r"sig-F [$\mu$V]")
    leg = ax.legend(fontsize=7, frameon=False, loc="upper center", ncol=3, handlelength=1.5, columnspacing=1.2)
    for line in leg.get_lines():
        line.set_linewidth(1.5)
    fig.savefig(FIG_DIR / "lp_time.pdf")
    plt.close(fig)

    # frequency domain: single-sided amplitude spectra, whole recording
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    for z, color, lw, label in ((raw, RAW_COLOR, 0.4, "raw"), (hp, HP_COLOR, 0.4, "HP"),
                                (lp, ECG_COLOR, 0.4, "HP + LP")):
        x = z - z.mean()
        N = len(x)
        A = 2 * np.abs(np.fft.rfft(x)) / N
        fk = np.fft.rfftfreq(N, 1 / FS)
        ax.loglog(fk[1:], A[1:], color=color, lw=lw, label=label)
    ax.set_xlim(fk[1], FS / 2)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$2|X[k]|/N$ [$\mu$V]")
    leg = ax.legend(fontsize=7, frameon=False, loc="lower left")
    for line in leg.get_lines():
        line.set_linewidth(1.5)
    fig.savefig(FIG_DIR / "lp_freq.pdf")
    plt.close(fig)
