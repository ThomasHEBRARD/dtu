clear
close all
addpath GraphCut functions

%%
path = '../../../../Data/week5/';
GT = imread([path, 'noise_free_circles.png']); % ground truth
I = imread([path, 'noisy_circles.png']);
mu = unique(GT); % instead of estimating 

% converting all to double
GT = double(GT)/255;
I = double(I)/255;
mu = double(mu)/255;

beta = 0.05;
U = [(I(:)-mu(1)).^2, (I(:)-mu(2)).^2, (I(:)-mu(3)).^2];
[~, S0] = min(U, [], 2);
S0 = reshape(S0, size(I));
S = multilabel_MRF(U, size(I), beta);

D0 = mu(S0);
D = mu(S); % denoised image using intensities from mu

figure
subplot(2,2,1), imagesc(GT, [0,1])
axis image, colormap gray, title('noise-free')
subplot(2,2,2), imagesc(I, [0,1])
axis image, colormap gray, title('noisy')
subplot(2,2,3), imagesc(D0, [0,1])
axis image, colormap gray, title('max likelihood')
subplot(2,2,4), imagesc(D, [0,1])
axis image, colormap gray, title('max posterior')



