function [g, dg, ddg, dddg] = getGaussDerivative(t)
% Computes kernels of Gaussian and its derivatives. Takes the variance as input.
    kSize = 5;
    s = sqrt(t);
    x = -ceil(s*kSize):ceil(s*kSize);
    g = exp(-x.^2/(2*t));
    g = g/sum(g);
    dg = -x/(t).*g;
    ddg = -g/(t) - x/(t).*dg;
    dddg = -dg/(t) - dg/(t) - x/(t).*ddg;

end