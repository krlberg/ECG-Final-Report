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
- Same check applied elsewhere (TA-style review): drift source (2a), noise source above 40 Hz (3a), why the 11-13% lower
  R peak is accepted (3d), cause of the dips at +-0.075 s (4a), why the dips deepen after filtering (4b).

## Repo
- This repo (https://github.com/krlberg/ECG-Final-Report, private) is synced with Overleaf: `main.tex` at the root is the report.
  Two remotes: `origin` (GitHub) and `overleaf` (Overleaf git, https://git.overleaf.com/6ac16274b1b29fb31b659c5c,
  branch `main`; token in the macOS keychain, never write it into files). Local setup on the user's Mac: a
  `.git/hooks/post-commit` hook pushes every commit to both remotes, and `git sync` pulls Overleaf + GitHub and pushes
  to both. Run `git sync` BEFORE editing (the user may edit in Overleaf). No need for Overleaf's Menu > GitHub any more.
  Cloud sessions have no Overleaf remote: push to GitHub only. Always check `latexmk -pdf main.tex` compiles first.
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
- Filters (`code/filters.py`, shared by Q2-Q5): HP = 2nd-order Butterworth IIR (bilinear transform), 0.5 Hz,
  applied ONCE causally (lfilter) after removing the mean. No forward-backward/zero-phase filtering: the reader
  (12.4) says the course does not use it (changed 16 Oct 2026). LP = Hamming-window FIR, K = 201, 40 Hz (-6 dB),
  output shifted back by (K-1)/2 = 100 samples (centred convolution, reader eq. 12.8).
  sig-F SNR: raw -0.4 dB, HP 10.0 dB, HP+LP 17.2 dB. The HP phase (30 deg = 60 ms at f_HR) shifts the xcorr maxima
  to -0.21/+0.51 s (Phase 2: -0.25/+0.41 s), now one period apart, so the old T-wave explanation of the 0.67 s
  spacing is dropped. The averaged pulse wave (max 0.41 s after R) confirms the true delay. ACF unaffected.
- Reader level: keep explanations to what the reader covers (no window side-lobe/transition formulas, no SOS,
  no impulse-response symmetry arguments, no zero-phase filtering).
- Correlations (`code/q4_acf.py`, `code/q5_xcorr.py`): same window (36.5-41.5 s) and normalisation as Phase 2; sig-P unfiltered.
- Figures: one style (blue = filtered, grey = unfiltered, no arrows, legend above the plot, only required annotations).

## Workflow and status
- User rules (16 Oct 2026), ALWAYS follow:
  1. `git sync` before editing; commit after every change (the hook pushes to GitHub and Overleaf).
  2. EVERYTHING Claude adds or changes in main.tex goes in blue: wrap it in `\chg{...}` (macro in the preamble),
     including captions and table entries. Keep existing `\chg` marks until the user says the review is done.
     Before submission switch the macro to `\newcommand{\chg}[1]{#1}` (or remove the wrappers).
- One agent per question drafts code + figures + text; the main session merges into main.tex, checks the rendered PDF, pushes.
  A strict "TA" grader agent reviews; an editor agent checks for AI-like writing and unnecessary content.
- Status: DONE (see the latest round below). Earlier independent grade (grader5): 9.5 / 9.5 / 9.0 / 9.5 / 9.0, predicted 9.3; its 3 must-fixes
  (3d 50 Hz wording, 5b lag change < 0.01 s, 5d "pulse peak") applied -> ~9.5.
  Skipped optional: a 3f caveat on in-band noise. Target: 9.5/10 per section.
- 13 Oct 2026 grading round (3 independent graders, after the Phase 2 feedback fixes): A (strict TA) 9.2, B (technical,
  re-ran all numbers) 9.0, C (completeness/conciseness) 9.2. Applied, all verified against the data: 2a drift lies mainly
  below 0.5 Hz (not 0.3), 2b 32 dB at 0.2 Hz, 5b rewritten (removed drift slightly correlated with sig-P cancels the 3%
  normalisation gain at the maxima; lags change <= 0.005 s; -0.25 s max = 0.47 s after previous R), 5c explains the
  -0.28 minimum at -0.46 s (pulse-wave minimum ~0.25 s after R), Fig. 1 shows B_s edges and the SNR value, 1a why sig-P
  is highest (4% vs 49% power below 0.5 Hz), 3d K = 201 motivated (K = 401/45 Hz gains only ~2 points of R-peak loss),
  3e H = |H_HP|^2 H_LP, captions of Fig. 2/4 say zero phase, cuts in 3f/5d. Figure font pinned to DejaVu Sans.
- Confirmation round on the fixed report: 2 fresh graders, both 9.2 (9.0 / 9.5 / 9.0 / 9.5 / 9.0), no wrong numbers.
  Applied: 5b quotes 3-decimal values (rounded ones seemed to contradict "<= 0.005 s" / "< 0.01"), 3a "clearly visible
  up to about 30 Hz", 3d R-peak loss 11-13% (median 13% over 64 beats), 3f now has the in-band-noise caveat.
- Push to 9.5 (after the 9.2 rounds): 1a justifies the 0.5-40 Hz band for sig-P (0.17% of its power in 7-40 Hz, SNR same
  for 0.5-10 Hz); 5b explains why the xcorr maxima are 0.67 s apart (pulse wave also lines up with the T wave; without
  the T-wave region they lie at -0.31/+0.40 s; NOT a varying beat interval, RR is 0.70-0.725 s); 5c lists the two new
  observations beyond Phase 2 explicitly (filtering vs shape; pulse starts rising ~0.2 s and peaks ~0.4 s after R);
  Fig. 2 marks 0.3 Hz / -18.8 dB. Checks in `code/q5_timing.py`. Note: regenerating figures here can shift the bbox by
  1-2 px (matplotlib version); only commit figures that actually changed.
- Regrade on that version: both 9.3 (9.5 / 9.5 / 9.5 / 9.0 / 9.0). Applied their must-fixes for 2.3.4/2.3.5: 4a says why the
  ACF peaks are narrow and that -0.17 is only the zero-lag dip (side-peak dips -0.11..-0.14); 5b describes the T-wave test
  (sig-F zeroed 0.10-0.45 s after each R) and is shortened; 5c links -0.46 s (0.26 s after R) to the measured pulse
  minimum 0.22 s / maximum 0.41 s after R (removing the T wave does NOT move the xcorr minimum, so no T-wave claim there);
  3a: -44 dB at 48 Hz, -53.5 dB at 50 Hz (48 Hz is not yet the stop band); Fig. 1 caption "vertical lines".
- Confirmation round on that version: strict TA 9.5 (9.5 in every section, no must-fixes), lecturer 9.4 (9.5 except
  2.3.5 at 9.0 only for the dense 5b). Then applied: 5b split into short sentences + paragraph break (lags / amplitudes),
  5c "broader and much lower", 5d "period of 0.72 s, which matches f_HR". Expected grade ~9.5.
  Unapplied nice-to-haves: mark maxima/minimum in Fig. 7; motivate K in 3a (now in 3d).
- 16 Oct 2026 (local session): switched to the causal HP, reran Q2-Q5, simplified text to reader level, merged with
  the 13 Oct rounds above (their explanations kept, numbers updated: 2b, 3d R-peak loss ~13% median over 59 beats,
  K = 401/45 Hz gives 10.6%; 5b/5c/5d rewritten for the HP phase shift). Earlier grades were for the zero-phase version.
  Grader on the merged version: 9.5 / 9.3 / 9.5 / 9.5 / 9.0 (~9.35); applied its must-fixes (2e +0.5 dB, 5b cause of
  lower maxima / deeper minimum = frequency-dependent HP phase changes the slow ECG shape) and optional 5c/5d/3d/2b wording.
  Then added: phase panel in Fig. 2 (30 deg at f_HR, 4 deg at 10 Hz), dots on the quoted maxima/minimum in Fig. 7.
  Reader-level audit (16 Oct): nothing clearly beyond the course. Applied its cuts: no beat-averaged pulse wave
  (extra method, not in the course; 5c/5d use the Phase 2 xcorr maximum +0.41 s), "does not affect" instead of
  "cancels" for the ACF (no Wiener-Khinchin), no h[n]-symmetry wording in 3a, no K = 401 comparison in 3d,
  shorter 1a/3a/3c/3e/5b. 4a must stay at 3 sentences (manual: 2-3).
  1a rework (16 Oct): method written as 4 steps (mean removed + DFT; P[k] with bin spacing f_s/N = 0.022 Hz and
  Parseval; band split; 10 log10 ratio), band edges motivated, "Important points when calculating the SNR" with
  Band / DC offset / Segment length. Fig. 1 is now `figures/snr_all.pdf` (2x2, all four signals, totals + SNR per
  panel); `snr_F.pdf` removed. Report is 7 pages (no page limit).
- Before submitting: check Canvas for a rubric or page limit (none found locally).
