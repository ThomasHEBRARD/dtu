% Vedrana Andersen Dahl (vand@dtu.dk) 
% Anders Bjorholm Dahl (abda@dtu.dk)

path = '../../../../Data/week3/3labels/'; % replace with path to your repository

tic
% TRAING THE MODEL
training_image = double(imread([path,'training_image.png']));
training_labels = imread([path,'training_labels.png']);
[~,~,l] = unique(training_labels);
training_labels = reshape(l,size(training_labels));
nr_labels = max(training_labels(:)); % number of labels in the training image

figure, subplot(1,2,1)
imagesc(training_image), colormap(gca,'gray'), axis image
title('training image')
subplot(1,2,2)
imagesc(training_labels), colormap(gca,'jet'), axis image
title('labels for training image')

sigma = [1,2,4]; % standard deviation for gaussian features
features = get_gauss_feat_multi(training_image,sigma);
features = reshape(features, [], size(features,3));
labels = training_labels(:);
 
nr_keep = 10000; % number of features randomly picked for clustering 
keep_indices = randperm(size(features,1),nr_keep);
features_subset = features(keep_indices,:);
labels_subset = labels(keep_indices);
 
nr_clusters = 500; % number of feature clusters
[assignment, cluster_centers] = kmeans(features_subset, nr_clusters);
edges = (0:nr_clusters)+0.5; % histogram edges halfway between integers
hist = zeros(nr_clusters,nr_labels);
for l = 1:nr_labels
    hist(:,l) = histcounts(assignment(labels_subset==l),edges);
end
sum_hist = sum(hist,2);
cluster_probabilities = hist./sum_hist;
 
figure, subplot(1,2,1)
legend_label = [repmat('label ',[nr_labels,1]),  num2str((1:nr_labels)')];
plot(hist,'.')
xlabel('cluster id')
ylabel('number of features in cluster')
legend(legend_label)
title('features in clusters per label')
subplot(1,2,2)
plot(cluster_probabilities,'.')
xlabel('cluster id')
ylabel('label probability for cluster')
legend(legend_label)
title('cluster probabilities')
 
%  Finished training
% 
%% USING THE MODEL
testing_image = double(imread([path,'testing_image.png']));

features_testing = get_gauss_feat_multi(testing_image,sigma);
features_testing = reshape(features_testing, [], size(features_testing,3));
assignment_testing = knnsearch(cluster_centers,features_testing);
probability_image = zeros(numel(assignment_testing), nr_labels);
for l = 1:nr_labels
    probability_image(:,l) = cluster_probabilities(assignment_testing, l);
end
probability_image = reshape(probability_image, [size(testing_image), nr_labels]);

P_rgb = zeros(size(probability_image,1),size(probability_image,2),3);
k = min(nr_labels,3);
P_rgb(:,:,1:k) = probability_image(:,:,1:k);

figure, subplot(1,2,1)
imagesc(testing_image), colormap(gca, 'gray'), axis image
title('testing image')
subplot(1,2,2)
imagesc(P_rgb), axis image
title('probabilities for testing image as RGB')

disp(toc)

%%  SMOOTH PROBABILITY MAP

sigma = 3; % Gaussian smoothing parameter

[~,seg_im_max] = max(P_rgb,[],3);
P_rgb_max = zeros(size(P_rgb));
for i = 1:size(P_rgb,3)
    P_rgb_max(:,:,i) = seg_im_max == i;
end
figure,imagesc(P_rgb_max)

probability_smooth = zeros(size(probability_image));
for i = 1:size(probability_image,3)
    probability_smooth(:,:,i) = imgaussfilt(probability_image(:,:,i),sigma);
end
[~,seg_im_smooth] = max(probability_smooth,[],3);

figure,imagesc(seg_im_smooth)


probability_smooth_max = zeros(size(probability_image));
for i = 1:size(probability_image,3)
    probability_smooth_max(:,:,i) = seg_im_smooth == i;
end
figure,imagesc(probability_smooth_max)

P_rgb_smooth = zeros(size(probability_smooth_max,1), size(probability_smooth_max,2), 3);
k = min(nr_labels,3);
P_rgb_smooth(:,:,1:k) = probability_smooth(:,:,1:k);
P_rgb_smooth_max = zeros(size(probability_smooth_max,1), size(probability_smooth_max,2), 3);
P_rgb_smooth_max(:,:,1:k) = probability_smooth_max(:,:,1:k);
 
% Display result
figure
subplot(241)
imagesc(P_rgb(:,:,1)), axis image
subplot(242)
imagesc(P_rgb(:,:,2)), axis image
subplot(243)
imagesc(P_rgb(:,:,3)), axis image
subplot(244)
imagesc(P_rgb_max), axis image
subplot(245)
imagesc(P_rgb_smooth(:,:,1)), axis image
subplot(246)
imagesc(P_rgb_smooth(:,:,2)), axis image
subplot(247)
imagesc(P_rgb_smooth(:,:,3)), axis image
subplot(248)
imagesc(P_rgb_smooth_max), axis image
