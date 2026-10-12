"""Question 2 (manual 2.3.2): high-pass filter of sig-F (design in filters.py).

Response: sosfiltfilt runs the filter forward and backward, so the effective response is |H|^2.
Signal: raw vs high-pass sig-F, 35-45 s and power spectra of the whole recording.
SNR: same method as q1a, plus a small sweep of f_c and order.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss

from ecg_data import ECG_COLOR, FIG_DIR, FS, INK, INK_2, style
from filters import HP_FC, HP_ORDER, HP_SOS, filtered_F
from q1a_snr import power_spectrum, snr_db

F_HR = 1.40  # Hz, heart rate from Phase 2
F_DRIFT = 0.3  # Hz, drift lies below this (Phase 2)
T0, T1 = 35.0, 45.0  # s, same window as question 2a
RAW_COLOR = "#a3a29e"

style()
t, raw, hp, _ = filtered_F()

# ---- SNR ------------------------------------------------------------------------------------
print(f"sig-F raw:       SNR = {snr_db(*power_spectrum(raw)):.1f} dB")
print(f"sig-F high-pass: SNR = {snr_db(*power_spectrum(hp)):.1f} dB")
for order in (2, 4):
    for fc in (0.3, 0.5, 0.7):
        sos = ss.butter(order, fc, "highpass", fs=FS, output="sos")
        y = ss.sosfiltfilt(sos, raw)
        print(f"  order {order}, f_c = {fc} Hz: SNR = {snr_db(*power_spectrum(y)):.1f} dB")

# ---- (b) effective magnitude response |H|^2 -------------------------------------------------
f = np.logspace(-2, np.log10(100), 2000)
_, h = ss.sosfreqz(HP_SOS, worN=f, fs=FS)
G = 2 * 20 * np.log10(np.abs(h))  # dB of |H|^2 (forward-backward)
G_hr = 2 * 20 * np.log10(np.abs(ss.sosfreqz(HP_SOS, worN=[F_HR], fs=FS)[1][0]))

fig, ax = plt.subplots(figsize=(4.2, 2.4))
ax.axvspan(f[0], F_DRIFT, color=INK_2, alpha=0.10, lw=0)
ax.text(0.03, -75, "drift", color=INK_2, fontsize=7.5, ha="center", va="bottom")
ax.semilogx(f, G, color=ECG_COLOR, lw=1.2)
ax.plot(HP_FC, -6, "o", ms=3, color=INK, zorder=3)
ax.annotate(rf"$f_c$ = {HP_FC} Hz, $-6$ dB", (HP_FC, -6), xytext=(15, -40), textcoords="offset points",
            fontsize=7.5, color=INK_2, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.6, shrinkA=1, shrinkB=3))
ax.plot(F_HR, G_hr, "o", ms=3, color=INK, zorder=3)
ax.annotate(rf"$f_\mathrm{{HR}}$ = {F_HR:.2f} Hz, ${G_hr:.1f}$ dB", (F_HR, G_hr), xytext=(12, -14),
            textcoords="offset points", fontsize=7.5, color=INK_2, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.6, shrinkA=1, shrinkB=3))
ax.set_xlim(f[0], f[-1])
ax.set_ylim(-80, 5)
ax.set_xlabel("f [Hz]")
ax.set_ylabel(r"$|H(f)|^2$ [dB]")
fig.savefig(FIG_DIR / "hp_response.pdf")
plt.close(fig)

# ---- (d) time domain ------------------------------------------------------------------------
win = (t >= T0) & (t < T1)
fig, ax = plt.subplots(figsize=(3.1, 2.0))
ax.plot(t[win], raw[win] - raw[win].mean(), color=RAW_COLOR, lw=0.6, label="raw (mean removed)")
ax.plot(t[win], hp[win], color=ECG_COLOR, lw=0.6, label="high-pass")
ax.set_xlim(T0, T1)
ax.set_ylim(-350, 1250)  # room for the legend
ax.set_xlabel("t [s]")
ax.set_ylabel(r"sig-F [$\mu$V]")
ax.legend(fontsize=7, loc="upper left", frameon=False, ncol=2, handlelength=1.2, columnspacing=1.0)
fig.savefig(FIG_DIR / "hp_time.pdf")
plt.close(fig)

# ---- (d) frequency domain -------------------------------------------------------------------
fr, P_raw = power_spectrum(raw)
_, P_hp = power_spectrum(hp)
fig, ax = plt.subplots(figsize=(3.1, 2.0))
ax.loglog(fr[1:], P_raw[1:], color=RAW_COLOR, lw=0.4, label="raw")
ax.loglog(fr[1:], P_hp[1:], color=ECG_COLOR, lw=0.4, label="high-pass")
ax.axvline(HP_FC, color=INK_2, lw=0.6, ls="--")
ax.text(HP_FC * 1.15, 1e-7, "$f_c$", color=INK_2, fontsize=7.5)
ax.set_xlim(fr[1], FS / 2)
ax.set_xlabel("f [Hz]")
ax.set_ylabel(r"$P[k]$ [$\mu$V$^2$]")
ax.legend(fontsize=7, loc="upper right", frameon=False)
fig.savefig(FIG_DIR / "hp_freq.pdf")
plt.close(fig)
