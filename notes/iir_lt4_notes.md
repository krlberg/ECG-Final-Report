# Notes for Q2/Q3 (filters) from LT4 and iirblt.m

- LT4 (IIR, "extreme" spec): band-pass [0.2pi, 0.4pi], <=3 dB ripple, >=90 dB stopband, budgets 2x8/10/12 coeffs.
  Conclusion (verbatim): "This calculation shows the low number of coefficients an IIR filter needs to meet a sharp
  transition band. A FIR filter would need much more coefficients. However, do notice its strong non-linear phase behaviour."
  Figure = freqz magnitude (dB) + phase vs normalised frequency (x pi rad/sample); looks elliptic.
- iirblt.m: hand BLT of a 2nd-order analogue filter, s = 2 fs (1 - z^-1)/(1 + z^-1), omega = 2 pi f in rad/s
  (NOT f, NOT 2 pi f/fs). Result written as difference equation y[n]+a1 y[n-1]+a2 y[n-2] = b0 x[n]+b1 x[n-1]+b2 x[n-2];
  checked against Matlab bilinear(). No pre-warping.
- Warping at fs = 1024 Hz is negligible: 0.3 Hz ~3e-5 %, 30 Hz 0.28 %, 50 Hz 0.79 %.
- Practical (not from course files):
  - HP at 0.3-0.5 Hz: Omega_c ~ 6-10e-4 pi, poles near z = 1 -> use low-order Butterworth (monotonic, no ripple
    on the 1.4 Hz fundamental) in SOS form; expect long start-up transient.
  - Zero-phase filtfilt squares |H| (dB doubles, -3 dB -> -6 dB); reader says course does not use it -> justify if used.
  - LP: passband ~30-40 Hz, stopband 50 Hz; choose order with buttord/ellipord ("search" idea of LT4).
  - Two steps vs band-pass: LTI cascade H_BP = H_HP H_LP, order irrelevant; single BP no selectivity gain, worse numerically.
- lt1 (Fourier/RC LP, -3 dB, Parseval) and lt2 (sampling, aliasing, backward-difference discretisation): marginal.
