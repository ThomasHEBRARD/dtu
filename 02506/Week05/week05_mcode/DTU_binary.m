clear, close all, rng(0)
addpath 'functions' 'GraphCut'

% noisy image
path = '../../../../Data/week5/';
I = double(imread([path,'DTU_noisy.png']))/255; 

% MRF parameteers
beta = 0.1; 
mu = [90, 170]/255;

% Internal and external edges
dim = size(I);
indices = reshape(1:prod(dim), dim);
edge_x = indices(1:end-1,:);
edge_y = indices(:,1:end-1);
edge_n = [edge_x(:), edge_x(:)+1, beta*ones(numel(edge_x),2);
    edge_y(:),edge_y(:)+dim(1), beta*ones(numel(edge_y),2)];
U = [(double(I(:)) - mu(1)).^2, (double(I(:)) - mu(2)).^2];
edge_t = [(1:numel(I))', U]; 

% Graph cut
S = false(size(I));
S(GraphCutMex(numel(I),edge_t,edge_n)) = true;

% Visualizatin
subplot(131), imagesc(I), axis image, colormap gray, title('noisy image')
title({'Noisy image'})
subplot(132), imagesc(S), title('Segmented'), axis image
subplot(133), segmentation_histogram(I, S, linspace(0,1,256)), axis square
title({'Segmentation histogram'})



