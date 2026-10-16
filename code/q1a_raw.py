"""Question 1a: the four raw signals over a 10 s window, one figure per signal."""
import matplotlib.pyplot as plt

from ecg_data import CHANNELS, ECG_COLOR, FIG_DIR, PLETH_COLOR, load, style

T0, T1 = 35.0, 45.0  # s, cleanest stretch of the record (no movement artefacts)

style()
t, sig = load()
win = (t >= T0) & (t < T1)

for key, (_, name) in CHANNELS.items():
    fig, ax = plt.subplots(figsize=(3.1, 2.0))
    if key == "P":
        ax.plot(t[win], sig[key][win], color=PLETH_COLOR, lw=0.8)
        ax.set_ylabel(f"{name} [a.u.]")
    else:
        # raw values in uV; the DC offset is kept on purpose
        ax.plot(t[win], sig[key][win], color=ECG_COLOR, lw=0.6)
        ax.set_ylabel(f"{name} [$\\mu$V]")
    ax.set_xlabel("t [s]")
    ax.set_xlim(T0, T1)
    fig.savefig(FIG_DIR / f"raw_{key}.pdf")
    plt.close(fig)
