function imfeat = get_gauss_feat_multi(im, s, normalize)
% Gauss derivative feaures for every image pixel.
% imfeat = get_gauss_feat_im(im, s, normalize)
%    Inputs:
%        im: a 2D image, size (r,c).
%        sigma: array of n standard deviations for Gaussian derivatives.
%        normalize: optional flag indicating normalization of features.
%    Output:
%        imfeat: a 3D array of size (r,c,n*15) with a n*15-dimentional feature
%            vector for every image pixel.

if nargin<3
    normalize = true;
end
n = size(s,2);
imfeat = zeros(size(im,1),size(im,2),15*n);
t = 0;
for i = 1:n
    f = t+1;
    t = i*15;
    imfeat(:,:,f:t) = get_gauss_feat_im(im,s(i),normalize);
end
    

if normalize
    imfeat = imfeat - mean(imfeat,[1,2]);
    imfeat = imfeat./std(imfeat,0,[1,2]);
end
