% IIR/BLT
fs=16000;
f1=1000;
f2=3000;

% Note the relationship between w [rad/s] and f [Hz]
% Common error 1: 
% Claiming w1=f1 etc.
% Common error 2:
% Claiming w1=2 pi f/fs. That is wrong for two reasons
% a. Omega=2 pi f /fs would be in rad/sample (=normalized or discrete
% frequency)
% b. Relationship in a. between Omega and f,fs does not hold if you do
% bilinear transformation (BLT), only if you sample from a continuous signal.
% Example x(t)=cos(wt), then 
% x[n]=x(nTs)=cos(wnTs)=cos([wTs]n). Use wTs=2 pi f Ts=2 pi f/fs=Omega. 
% so x[n]=cos(Omega n). Moral: Omega1=2 pi f/fs holds if you sample, 
% but does **not*** hold in the context of BLT
w1=2*pi*f1;
w2=2*pi*f2;

% now substitute either s=2fs((z-1)/(z+1)) or s=2fs(1(1-z^{-1})/(1+z^{-1})
% in H(s), together with w1=2 pi f1, w2=2 pi f2.
% My personal choice is the latter one, since after substitution and
% rewriting you can read of the difference equation very easily:
% if H[z]=(b0+b1z^{-1}+b2z^{-2})/(1+a1z^{-1}+a2z^{-2})=Y[z]/X[z] 
% so Y[z](1+a1z^{-1}+a2z^{-2})=X(z)(b0+b1z^{-1}+b2z^{-2}) in z-domain, so
% y[n]+a1y[n-1]+a2y[n-2]=b0x[n]+b1x[n-1]+b2x[n-2] in "n"-domain.
% Note, it is convention to normalize such that the coefficient in front of y[n]
% becomes 1. Perform substitution s=2fs(1(1-z^{-1})/(1+z^{-1}) in H(s) and rewrite

% raw a0 value, divide every term by this value 
a0raw=4*fs*fs+2*fs*(w2-w1)+w1*w2; 
% a and b collected in two vectors, ai/bi is coefficient of y[n-i]/x[n-i] term
% calc b and normalize
% [b0 b1 b2]
b=[(4*fs*fs*w1*w2)/a0raw (-8*fs*fs*w1*w2)/a0raw (4*fs*fs*w1*w2)/a0raw]; 
% calc a and normalize
% [a0 a1 a2] (Note first is not needed since answer will be 1)
a=[(4*fs*fs+2*fs*(w2-w1)+w1*w2)/a0raw  (-8*fs*fs+2*w1*w2)/a0raw (4*fs*fs-2*fs*(w2-w1)+w1*w2)/a0raw]; 

% Use freqz function that takes the filter coefficients and 
% calculates H(e^{j Omega}), H[z] with z=e^{j Omega}
subplot(1,2,1);
[H,W]=freqz(b,a);
plot(W, abs(H));
xlim([0 pi]);
xlabel('$\Omega$','interpreter','latex')
ylabel('$H(e^{j\Omega})$','interpreter','latex')
title('Human made');

% Matlab has a builtin function.....
% Specify H(s)
bs=[w1*w2 0 0];
as=[1 (w2-w1) w1*w2];
[b2, a2]=bilinear(bs, as, fs);

subplot(1,2,2);
[H2,W2]=freqz(b2,a2);
plot(W2, abs(H2));
xlim([0 pi]);
xlabel('$\Omega$','interpreter','latex')
ylabel('$H(e^{j\Omega})$','interpreter','latex')
title('Matlab made');

% Verify you have obtained exactly the same frequency response!
% The LDE that implements this filter is (see above)
% y[n]-1.1726y[n-1]+0.4793y[n-2]=10^8(0.7852x[n]-1.5704x[n-1]+0.7852x[n-2])