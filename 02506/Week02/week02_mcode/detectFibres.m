function [coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude)
% Detects fibers in images by finding maxima of Gaussian smoothed image
% Input:
%     im : Image.
%     diameterLimit : 2 x 1 vector of limits of diameters of the fibers (in pixels).
%     stepSize : step size in pixels.
%     tCenter : Scale of the Gaussian for center detection.
%     thresMagnitude : Threshold on blob magnitude.
% 
% Output:
%    coord : n x 2 array of coordinates with row and column coordinates in each column.
%    scale : n x 1 array of scales t (variance of the Gaussian).
% 
% Anders B. Dahl, abda@dtu.dk
% 


radiusLimit = diameterLimit/2;
radiusSteps = radiusLimit(1):stepSize:radiusLimit(2);
tStep = (radiusSteps.^2)/sqrt(2);

[r,c] = size(im);
n = size(tStep,2);
L_blob_vol = zeros(r,c,n);

for i = 1:n
    [g,~,ddg] = getGaussDerivative(tStep(i));
    L_blob_vol(:,:,i) = tStep(i)*(imfilter(imfilter(im, ddg, 'replicate'), g', 'replicate') + ...
        imfilter(imfilter(im, ddg', 'replicate'), g, 'replicate'));
end

% Detect fibre centers

g = getGaussDerivative(tCenter);
Lg = imfilter(imfilter(im, g, 'replicate'), g', 'replicate');

imregmax = imregionalmax(Lg);
[ctR,ctC] = find(imregmax == 1);

% Find coordinates and size (scale) of fibres

[magnitudeIm, scaleIm] = min(L_blob_vol,[],3);
scale = scaleIm((ctC-1)*r + ctR);
magnitude = -magnitudeIm((ctC-1)*r + ctR);
idx = magnitude > thresMagnitude;
coord = [ctR(idx), ctC(idx)];
scale = tStep(scale(idx))';







