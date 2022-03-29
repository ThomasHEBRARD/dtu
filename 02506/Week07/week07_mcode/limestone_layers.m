clear, close all
addpath GraphCut functions
RGB = imread('../../../../Data/week7/rammed-earth-layers-limestone.jpg');

figure
subplot(2,2,1)
imagesc(RGB), axis image
title('Input')

I = rgb2gray(RGB);
P = permute(I,[2,3,1]); % making sure that up is the third dimension

%% SETTINGS FOR GEOMETRIC CONSTRAINS
delta = 1; % smoothness very constrained, try also 3 to see less smoothness
wrap = 0; % should be 0 for terren-like surfaces

%% DARKEST LINE
cost_S = P;
s = grid_cut(cost_S,[],delta,wrap,[]);
subplot(2,2,2)
imagesc(RGB), axis image ij, colormap gray, hold on
plot(1:size(RGB,2),permute(s,[1,3,2]), 'r', 'LineWidth',2)
title('Darkest line')

%% TWO DARK LINES
cost_S = cat(4,P,P);
s = grid_cut(cost_S,[], delta, wrap, [50 200]);
subplot(2,2,3)
imagesc(RGB), axis image ij, colormap gray, hold on
plot(1:size(RGB,2), permute(s, [1,3,2]), 'r', 'LineWidth', 2)
title('Two dark lines')

%% DARKEST REGION
cost_R = cat(4,255-P,P,255-P);
s = grid_cut([], cost_R, delta, wrap, [1 200]);
subplot(2,2,4)
imagesc(RGB), axis image ij, colormap gray, hold on
plot(1:size(RGB,2), permute(s,[1,3,2]), 'r', 'LineWidth', 2)
title('Dark region')

