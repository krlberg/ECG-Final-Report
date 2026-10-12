# ECG assignment, final report (Signals, MOD5, UT Advanced Technology)

## Report writing
- Bachelor-level assignment. Keep the report straightforward and concise.
- Impersonal style: never use "we", "our", "I" or "you" in the report (use passive/impersonal wording).
- Answer each question directly. Do not add details, background or extra analysis the question does not ask for.
- The report follows manual section 2.3 exactly: 5 sections (2.3.1-2.3.5), with (a), (b), ... paragraphs per question.
  The manual question sits as a LaTeX comment ("% Manual 2.3.x") above each paragraph; keep all 19 of these lines.
- No page limit is given (neither the manual nor Canvas). The only length rule is "2-3 sentences" in 2.3.4a.
- Use the course reader's notation: x[n], f_s, DFT X[k] (eq. 11.1), R_xy[n] = sum_m x[m] y[m-n] (eq. 10.21), FIR length K taps, convolution symbol \otimes.
- Report date: 16 October 2026. Authors: Kirill Rybkov, Malek Galal Hamed Mohamed Ghanem (one submission per group).

## Repo
- This repo (https://github.com/krlberg/ECG-Final-Report, private) is synced with Overleaf: `main.tex` at the root is the report.
  After pushing, the user pulls in Overleaf via Menu > GitHub. Always check `latexmk -pdf main.tex` compiles before pushing.
- `code/` scripts write figures to `figures/`. Run from anywhere: `python3 code/q2_highpass.py` etc. Needs numpy, pandas, matplotlib, scipy.
- `intermediate-report/`: the submitted Phase 2 report (do not change). Phase 2 numbers used for comparison come from it.

## Course material
- `provided/Signals_ECG_v1.8.pdf`: lab manual (questions in section 2.3; no rubric).
- `provided/AdvEngSignals_1v0.pdf`: course reader (FIR Ch. 12, IIR Ch. 14, correlation 10.8; printed page + 9 = PDF page).
- `provided/learning-tasks/`: LT3 (`lt3.pdf`, solution `lt3All.pdf`) = FIR design / SNR estimation, the SNR method the manual
  refers to; LT4 + `iirblt.m` = IIR design. `notes/iir_lt4_notes.md` summarises LT4 and the IIR example.

## Data
- `csv/20260902_122613.CSV`, f_s = 1024 Hz, 45.5 s. Channels: sig-P (Pleth, a.u.), sig-R/L/F (ExG1-3, uV).
- Loader and plot style: `code/ecg_data.py`.

## Decisions
- 1a SNR (`code/q1a_snr.py`): whole recording (N = 46648), mean removed, P[k] = 2|X[k]|^2/N^2; power in 0.5-40 Hz
  (all four signals) = signal, all other power = noise, SNR = 10 log10(P_s/P_n). Deviates from LT3's noise extrapolation
  because the noise is not white (mainly drift). Results: P 13.6 dB, R -1.3, L -5.6, F -0.4 -> sig-F is filtered.
- Filters (`code/filters.py`, shared by Q2-Q5): HP = 2nd-order Butterworth IIR, 0.5 Hz, SOS, zero-phase (sosfiltfilt);
  LP = Hamming-window FIR, K = 201, 40 Hz (-6 dB), centred convolution (delay removed, zero phase).
  sig-F SNR: raw -0.4 dB, HP 10.5 dB, HP+LP 22.7 dB.
- Correlations (`code/q4_acf.py`, `code/q5_xcorr.py`): same window (36.5-41.5 s) and normalisation as Phase 2; sig-P unfiltered.
- Figures: one style (blue = filtered, grey = unfiltered, no arrows, legend above the plot, only required annotations).

## Workflow and status
- One agent per question drafts code + figures + text; the main session merges into main.tex, checks the rendered PDF, pushes.
  A strict "TA" grader agent reviews; an editor agent checks for AI-like writing and unnecessary content.
- Status: DONE. Final independent grade (grader5): 9.5 / 9.5 / 9.0 / 9.5 / 9.0, predicted 9.3; its 3 must-fixes
  (3d 50 Hz wording, 5b lag change < 0.01 s, 5d "pulse peak") applied -> ~9.5.
  Skipped optional: a 3f caveat on in-band noise. Target: 9.5/10 per section.
- Before submitting: check Canvas for a rubric or page limit (none found locally).
