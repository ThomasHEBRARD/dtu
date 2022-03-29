% Simple script - will be replaced
% ABDA


clear, close all

%%

path = '../../../../Data/week1/fibres_xcth.png';

im = double(imread(path));

figure,imagesc(im), colormap gray, axis image

%%

t = 100;
s = sqrt(t);

x = (-ceil(s)*3):(ceil(s)*3);
g = 1/sqrt(pi*t*2) * exp(-x.^2/(2*t));
figure
plot(g)

%%

im_g = imfilter(im, g);
im_g = imfilter(im_g, g');

figure,imagesc(im_g),axis image

%%
g2d = g'*g;

im_g2d = imfilter(im, g2d);
figure,imagesc(im_g2d-im_g),axis image












