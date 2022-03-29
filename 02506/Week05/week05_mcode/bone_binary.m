clear
close all
addpath GraphCut functions


%% Inspect the image and the histogram
path = '../../../../Data/week5/';
I = double(imread([path,'V12_10X_x502.png']))/(2^16-1);
figure, imagesc(I), axis image, colormap gray

figure
edges = linspace(0, 1, 257);
histogram(I(:), edges, 'EdgeColor', 'none', 'FaceColor','k'), 
xlabel('pixel values'), ylabel('count'), title('intensity histogram')

%% Define likelihood
mu = [0.40, 0.71]; % estimated peaks of the distributions
U = [(I(:)-mu(1)).^2, (I(:)-mu(2)).^2];
[~, S0] = min(U, [], 2);  % max likelihood (thresholding between peaks)

dim = size(I);
S0 = reshape(S0,dim);
figure, imagesc(S0), axis image, title ('max likelihood')

%% Define prior, construct graph, solve
beta = 0.1;
indices = reshape(1:prod(dim),dim);
edge_x = indices(1:end-1,:,:);
edge_y = indices(:,1:end-1,:);
edge_n = [edge_x(:),edge_x(:)+1, beta*ones(numel(edge_x),2);
    edge_y(:),edge_y(:)+dim(1), beta*ones(numel(edge_y),2)];
edge_t = [indices(:),U]; % terminal edges

% solving
Scut = GraphCutMex(prod(dim),edge_t,edge_n);
S = ones(dim,'uint8');
S(Scut) = 2;

figure, imagesc(S), axis image, title('max posterior')

figure
segmentation_histogram(I, S, edges) 
xlabel('pixel values'), ylabel('count'), title('segmentation histogram')


