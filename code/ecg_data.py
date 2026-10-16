"""Load the CSV recording (TMSi PolyBench, 2 Sep 2026 12:26) and shared plot settings."""
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "csv" / "20260902_122613.CSV"
FIG_DIR = ROOT / "figures"  # final report figures (intermediate ones live in intermediate-report/figures)

FS = 1024.0  # Hz, fixed by the measurement protocol

# Channel order in the file follows the setup (channel 1, 2, 3, finger clip on 16).
CHANNELS = {
    "P": ("Pleth", "sig-P"),
    "R": ("ExG1 [uV]", "sig-R"),
    "L": ("ExG2 [uV]", "sig-L"),
    "F": ("ExG3 [uV]", "sig-F"),
}

ECG_COLOR = "#2a78d6"
PLETH_COLOR = "#eb6834"
INK = "#0b0b0b"
RED = "#d62728"  # Phase 2 (unfiltered) correlations, dashed
INK_2 = "#52514e"
GRID = "#d9d8d4"


def load():
    """Return time vector t [s] and dict of raw signals {key: array}.

    ECG channels in uV, pleth in arbitrary units. No offset removal.
    """
    df = pd.read_csv(CSV)
    sig = {k: df[col].to_numpy(dtype=float) for k, (col, _) in CHANNELS.items()}
    t = np.arange(len(df)) / FS
    return t, sig


def style():
    """Matplotlib settings for half-width subfigures in the report."""
    matplotlib.rcParams.update({
        "font.family": "DejaVu Sans",  # pinned so all figures use the same font on any machine
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.edgecolor": INK_2,
        "axes.labelcolor": INK,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
    })
