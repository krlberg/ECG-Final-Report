# ECG assignment, final report (Signals, MOD5, UT Advanced Technology)

## Report writing
- Bachelor-level assignment. Keep the report straightforward and concise.
- Impersonal style: never use "we", "our", "I" or "you" in the report (use passive/impersonal wording).
- Answer each question directly. Do not add details, background or extra analysis the question does not ask for.
- The report follows manual section 2.3 exactly: 5 sections (2.3.1-2.3.5), with (a), (b), ... paragraphs per question.
  The manual question sits as a LaTeX comment ("% Manual 2.3.x") above each paragraph; keep all 19 of these lines.
- No page limit is given (neither the manual nor Canvas). The only length rule is "2-3 sentences" in 2.3.4a.
- Use the course reader's notation: x[n], f_s, DFT X[k] (eq. 11.1), R_xy[n] = sum_m x[m] y[m-n] (eq. 10.21), FIR length K taps, convolution symbol \otimes.
- Do not mention the Learning Tasks in the report. Mention Phase 2 only where the manual asks for it (2.3.4b, 2.3.5b, 2.3.5c).
- Report date: 16 October 2026. Authors: Kirill Rybkov, Malek Galal Hamed Mohamed Ghanem (one submission per group).

## Mistakes to avoid (from the Phase 2 TA feedback, 32/35)
The TA never deducted for numbers, only for observations stated without their meaning or cause.
Always explain *why* / *what it represents*, not only *what* is seen. Do not remove these fixes:
- "Strong peaks in range 1-10 Hz, what could it represent?" -> 5d: heart rate (1.40 Hz) and its harmonics,
  which together form the P, QRS and T waves.
- "Why is the central (xcorr) peak shifted?" -> 5c: the pressure wave needs time to travel from heart to finger,
  so the pulse peak follows the ECG spike by ~0.4 s; 5b: the maximum at -0.25 s is the pulse of the previous beat.
- "Visibility of peaks in acorr vs xcorr?" -> 5c: acorr peaks narrow and clear (sharp QRS), xcorr peaks broad and
  low (smooth pulse wave, different shape).
- Same check applied elsewhere (TA-style review): drift source (2a), noise source above 40 Hz (3a), why the 12% lower
  R peak is accepted (3d), cause of the dips at +-0.075 s (4a), why the dips deepen after filtering (4b).

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
  because the noise is not white (mainly drift); the report does not discuss this (user's choice). Results: P 13.6 dB, R -1.3, L -5.6, F -0.4 -> sig-F is filtered.
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
- 13 Oct 2026 grading round (3 independent graders, after the Phase 2 feedback fixes): A (strict TA) 9.2, B (technical,
  re-ran all numbers) 9.0, C (completeness/conciseness) 9.2. Applied, all verified against the data: 2a drift lies mainly
  below 0.5 Hz (not 0.3), 2b 32 dB at 0.2 Hz, 5b rewritten (removed drift slightly correlated with sig-P cancels the 3%
  normalisation gain at the maxima; lags change <= 0.005 s; -0.25 s max = 0.47 s after previous R), 5c explains the
  -0.28 minimum at -0.46 s (pulse-wave minimum ~0.25 s after R), Fig. 1 shows B_s edges and the SNR value, 1a why sig-P
  is highest (4% vs 49% power below 0.5 Hz), 3d K = 201 motivated (K = 401/45 Hz gains only ~2 points of R-peak loss),
  3e H = |H_HP|^2 H_LP, captions of Fig. 2/4 say zero phase, cuts in 3f/5d. Figure font pinned to DejaVu Sans.
- Before submitting: check Canvas for a rubric or page limit (none found locally).
