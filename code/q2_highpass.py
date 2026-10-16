"""Question 2 (manual 2.3.2): high-pass filter of sig-F (design in filters.py).

Response: magnitude |H(f)| and phase of the causal filter (applied once).
Signal: raw vs high-pass sig-F, 35-45 s and power spectra of the whole recording.
SNR: same method as q1a, plus a small sweep of f_c and order.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, style
from filters import HP_A, HP_B, HP_FC, HP_ORDER, filtered_F
from q1a_snr import power_spectrum, snr_db

F_HR = 1.40  # Hz, heart rate from Phase 2
T0, T1 = 35.0, 45.0  # s, same window as question 2a
RAW_COLOR = "#a3a29e"  # grey: unfiltered signal


def legend(ax, n):
    """Legend in one row above the axes, with thick handles."""
    leg = ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=n, fontsize=8, frameon=False,
                    borderaxespad=0.2, handlelength=1.5, columnspacing=1.2)
    for line in leg.get_lines():
        line.set_linewidth(1.5)

style()
t, raw, hp, _ = filtered_F()

# ---- SNR ------------------------------------------------------------------------------------
print(f"sig-F raw:       SNR = {snr_db(*power_spectrum(raw)):.1f} dB")
print(f"sig-F high-pass: SNR = {snr_db(*power_spectrum(hp)):.1f} dB")
for order in (2, 4):
    for fc in (0.3, 0.5, 0.7):
        sos = ss.butter(order, fc, "highpass", fs=FS, output="sos")
        y = ss.sosfilt(sos, raw - raw.mean())  # causal, as the main filter (sos only for numerical safety at order 4)
        print(f"  order {order}, f_c = {fc} Hz: SNR = {snr_db(*power_spectrum(y)):.1f} dB")

# ---- (b) magnitude response |H| -------------------------------------------------------------
f = np.logspace(-2, np.log10(100), 2000)
_, h = ss.freqz(HP_B, HP_A, worN=f, fs=FS)
G = 20 * np.log10(np.abs(h))
h_hr = ss.freqz(HP_B, HP_A, worN=[F_HR], fs=FS)[1][0]
G_hr = 20 * np.log10(np.abs(h_hr))
at = lambda f0: 20 * np.log10(np.abs(ss.freqz(HP_B, HP_A, worN=[f0], fs=FS)[1][0]))
print(f"b = {np.round(HP_B, 5)}, a = {np.round(HP_A, 5)}")
print(f"|H| at 0.1 Hz {at(0.1):.1f} dB, 0.2 Hz {at(0.2):.1f} dB, 0.3 Hz {at(0.3):.1f} dB, f_c {at(HP_FC):.1f} dB, "
      f"f_HR {G_hr:.2f} dB, phase at f_HR {np.degrees(np.angle(h_hr)):.0f} deg "
      f"({np.angle(h_hr) / (2 * np.pi * F_HR) * 1e3:.0f} ms), phase at 10 Hz "
      f"{np.degrees(np.angle(ss.freqz(HP_B, HP_A, worN=[10.0], fs=FS)[1][0])):.1f} deg")

fig, ax = plt.subplots(figsize=(4.2, 2.4))
ax.semilogx(f, G, color=ECG_COLOR, lw=1.2)
for f0, g0, text, xy, ha, va in [(HP_FC, at(HP_FC), rf"$f_c$ = {HP_FC} Hz, ${at(HP_FC):.0f}$ dB", (-6, 0), "right", "center"),
                                 (F_HR, G_hr, rf"$f_\mathrm{{HR}}$ = {F_HR:.2f} Hz, ${G_hr:.1f}$ dB", (4, -6),
                                  "left", "top"),
                                 (0.3, at(0.3), rf"0.3 Hz, ${at(0.3):.1f}$ dB", (6, -2), "left", "top")]:
    ax.plot(f0, g0, "o", ms=3.5, color=INK, zorder=3)
    ax.annotate(text, (f0, g0), xytext=xy, textcoords="offset points", fontsize=8, color=INK, ha=ha, va=va)
ax.set_xlim(0.02, 50)
ax.set_ylim(-60, 5)
ax.set_xlabel("f [Hz]")
ax.set_ylabel(r"$|H(f)|$ [dB]")
fig.savefig(FIG_DIR / "hp_response.pdf")
plt.close(fig)

# ---- (d) time domain ------------------------------------------------------------------------
win = (t >= T0) & (t < T1)
fig, ax = plt.subplots(figsize=(3.1, 2.0))
ax.plot(t[win], raw[win] - raw[win].mean(), color=RAW_COLOR, lw=0.6, label="raw")
ax.plot(t[win], hp[win], color=ECG_COLOR, lw=0.6, label="high-pass")
ax.set_xlim(T0, T1)
ax.set_xlabel("t [s]")
ax.set_ylabel(r"sig-F [$\mu$V]")
legend(ax, 2)
fig.savefig(FIG_DIR / "hp_time.pdf")
plt.close(fig)

# ---- (d) frequency domain -------------------------------------------------------------------
fr, P_raw = power_spectrum(raw)
_, P_hp = power_spectrum(hp)
fig, ax = plt.subplots(figsize=(3.1, 2.0))
ax.loglog(fr[1:], P_raw[1:], color=RAW_COLOR, lw=0.5, label="raw")
ax.loglog(fr[1:], P_hp[1:], color=ECG_COLOR, lw=0.5, label="high-pass")
ax.set_xlim(fr[1], FS / 2)
ax.set_xlabel("f [Hz]")
ax.set_ylabel(r"$P[k]$ [$\mu$V$^2$]")
legend(ax, 2)
fig.savefig(FIG_DIR / "hp_freq.pdf")
plt.close(fig)
