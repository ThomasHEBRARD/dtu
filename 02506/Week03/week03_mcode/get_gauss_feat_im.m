function imfeat = get_gauss_feat_im(im, s, normalize)
% Gauss derivative feaures for every image pixel.
% imfeat = get_gauss_feat_im(im, s, normalize)
%    Inputs:
%        im: a 2D image, size (r,c).
%        sigma: standard deviation for Gaussian derivatives.
%        normalize: optional flag indicating normalization of features.
%    Output:
%        imfeat: a 3D array of size (r,c,15) with a 15-dimentional feature
%            vector for every image pixel.

if nargin<3
    normalize = true;
end
x = -ceil(4*s):ceil(4*s);

g = exp(-x.^2/(2*s^2));
g = g/sum(g);
dg = -x/(s^2).*g;
ddg = -1/(s^2).*g - x/(s^2).*dg;
dddg = -2/(s^2)*dg - x/(s^2).*ddg;
ddddg = -2/(s^2)*ddg - 1/(s^2).*ddg - x/(s^2).*dddg;

[r,c] = size(im);
imfeat = zeros(r,c,15);
imfeat(:,:,1) = imfilter(imfilter(im,g), g');
imfeat(:,:,2) = imfilter(imfilter(im,dg), g');
imfeat(:,:,3) = imfilter(imfilter(im,g), dg');
imfeat(:,:,4) = imfilter(imfilter(im,ddg), g');
imfeat(:,:,5) = imfilter(imfilter(im,g), ddg');
imfeat(:,:,6) = imfilter(imfilter(im,dg), dg');
imfeat(:,:,7) = imfilter(imfilter(im,dddg), g');
imfeat(:,:,8) = imfilter(imfilter(im,g), dddg');
imfeat(:,:,9) = imfilter(imfilter(im,ddg), dg');
imfeat(:,:,10) = imfilter(imfilter(im,dg), ddg');
imfeat(:,:,11) = imfilter(imfilter(im,g), ddddg');
imfeat(:,:,12) = imfilter(imfilter(im,dg), dddg');
imfeat(:,:,13) = imfilter(imfilter(im,ddg), ddg');
imfeat(:,:,14) = imfilter(imfilter(im,dddg), dg');
imfeat(:,:,15) = imfilter(imfilter(im,ddddg), g');

if normalize
    imfeat = imfeat - mean(imfeat,[1,2]);
    imfeat = imfeat./std(imfeat,0,[1,2]);
end
