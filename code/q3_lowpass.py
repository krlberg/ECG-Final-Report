"""Question 3 (manual 2.3.3): low-pass FIR filter (design in filters.py) applied to high-pass filtered sig-F.

Figures: magnitude response of the FIR, and raw / high-pass / high- + low-pass sig-F in time and frequency.
Prints the SNR of the three signals (same band and whole recording as question 1a).
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, style
from filters import LP_FC, LP_H, filtered_F
from q1a_snr import power_spectrum, snr_db

T0, T1 = 38.0, 40.5  # s, three beats inside the clean 35-45 s stretch
RAW_COLOR = "#a3a29e"  # grey: unfiltered signal
HP_COLOR = "#9cc2ee"  # light blue: high-pass only


def mark(ax, f0, dB, text, xytext, ha="left", va="center"):
    ax.plot(f0, dB, "o", ms=3.5, color=INK, zorder=3)
    ax.annotate(text, (f0, dB), xytext=xytext, textcoords="offset points", fontsize=8, color=INK, ha=ha, va=va)


def legend(ax, n):
    """Legend in one row above the axes, with thick handles."""
    leg = ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=n, fontsize=8, frameon=False,
                    borderaxespad=0.2, handlelength=1.5, columnspacing=1.2)
    for line in leg.get_lines():
        line.set_linewidth(1.5)


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
    ax.plot(f, H_dB, color=ECG_COLOR, lw=1.2)
    ax.set_xlim(0, 100)
    ax.set_ylim(-80, 5)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$|H(f)|$ [dB]")
    mark(ax, LP_FC, at(LP_FC), rf"$f_c$ = {LP_FC:.0f} Hz, ${at(LP_FC):.0f}$ dB", (6, 0))
    mark(ax, 50, at(50), f"50 Hz, ${at(50):.1f}$ dB", (6, 4), va="bottom")
    fig.savefig(FIG_DIR / "lp_response.pdf")
    plt.close(fig)

    # time domain: short stretch; raw with its window mean removed (large DC offset)
    win = (t >= T0) & (t < T1)
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    ax.plot(t[win], raw[win] - raw[win].mean(), color=RAW_COLOR, lw=0.6, label="raw")
    ax.plot(t[win], hp[win], color=HP_COLOR, lw=0.6, label="HP")
    ax.plot(t[win], lp[win], color=ECG_COLOR, lw=0.9, label="HP + LP")
    ax.set_xlim(T0, T1)
    ax.set_xlabel("t [s]")
    ax.set_ylabel(r"sig-F [$\mu$V]")
    legend(ax, 3)
    fig.savefig(FIG_DIR / "lp_time.pdf")
    plt.close(fig)

    # frequency domain: power per bin P[k] (as in questions 1a and 2), whole recording
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    for z, color, label in ((raw, RAW_COLOR, "raw"), (hp, HP_COLOR, "HP"), (lp, ECG_COLOR, "HP + LP")):
        fk, Pk = power_spectrum(z)
        ax.loglog(fk[1:], Pk[1:], color=color, lw=0.5, label=label)
    ax.set_xlim(fk[1], FS / 2)
    ax.set_xlabel("f [Hz]")
    ax.set_ylabel(r"$P[k]$ [$\mu$V$^2$]")
    legend(ax, 3)
    fig.savefig(FIG_DIR / "lp_freq.pdf")
    plt.close(fig)
