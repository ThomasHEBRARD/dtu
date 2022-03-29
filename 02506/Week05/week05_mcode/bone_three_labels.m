clear
close all
addpath GraphCut functions

%% Inspect the image and the histogram
path = '../../../../Data/week5/';
I = double(imread([path,'V12_10X_x502.png']))/(2^16-1);
figure, imagesc(I), axis image, colormap gray

edges = linspace(0, 1, 256);
histogram(I(:), edges, 'EdgeColor', 'none', 'FaceColor','k'), 
xlabel('pixel values'), ylabel('count'), title('intensity histogram')

%% Define likelihood
mu = [0.40, 0.46, 0.71];
dim = size(I);
U = [(I(:)-mu(1)).^2, (I(:)-mu(2)).^2, (I(:)-mu(3)).^2];
[~, S0] = min(U, [], 2);
S0 = reshape(S0, dim);
figure, imagesc(S0), axis image, title ('max likelihood')

%% Define prior and solve
beta = 0.02;
S = multilabel_MRF(U,dim,beta);
figure, imagesc(S), axis image, title('max posterior')

figure
segmentation_histogram(I, S, edges) 
xlabel('pixel values'), ylabel('count'), title('segmentation histogram')

