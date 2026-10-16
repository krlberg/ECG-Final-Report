# ECG Final Report

Signals module (MOD5) ECG assignment, final report. Authors: Kirill Rybkov, Malek Galal Hamed Mohamed Ghanem.
This repo is synced with Overleaf, so `main.tex` at the root is the final report.

## Layout

| Path | What it is |
|---|---|
| `main.tex` | Final report (Overleaf entry point) |
| `CLAUDE.md` | Writing rules, decisions and status for Claude sessions |
| `figures/` | Figures for the final report (scripts in `code/` write here) |
| `intermediate-report/` | Finished intermediate report (`main.tex` + its figures), for reference and reuse |
| `code/` | Python analysis scripts. `ecg_data.py` loads the recording and sets plot style; `q*_*.py` produce figures per question |
| `csv/` | Recording exported as CSV (TMSi PolyBench, 2 Sep 2026 12:26), fs = 1024 Hz. Channels: Pleth, ExG1 (R), ExG2 (L), ExG3 (F) |
| `poly5/` | Same recording in the raw Poly5 format (`data.S00`) with MATLAB readers |
| `provided/` | Course material: assignment PDF (`Signals_ECG_v1.8.pdf`), course reader (`AdvEngSignals_1v0.pdf`), `learning-tasks/` (LT1-4 + solutions, `iirblt.m`) and the provided reader scripts |
| `notes/` | Working notes (IIR design notes from LT4) |

## Running the code

```
pip install numpy pandas matplotlib scipy
python code/q1a_snr.py   # q2_highpass.py, q3_lowpass.py, q4_acf.py, q5_xcorr.py; run from anywhere
```
