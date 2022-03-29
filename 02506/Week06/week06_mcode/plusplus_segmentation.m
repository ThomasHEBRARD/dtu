clear
close all
addpath('functions')

filename = '../../../../Data/week6/plusplus.png';
I = double(rgb2gray(imread(filename)))/255;

nr_points = 100;
nr_iter = 100;
step_size = 10;
alpha = 0.01;
beta = 0.1;
center = (size(I)+1)/2;
radius = 0.3*mean(size(I));

%%

snake = make_circular_snake(center, radius, nr_points);
B = regularization_matrix(nr_points, alpha, beta);

figure
imagesc(I), axis image, colormap gray, hold on
plot(snake([1:end, 1], 2), snake([1:end, 1], 1), 'r', 'LineWidth', 2)
title('Initialization'), drawnow

for i=1:nr_iter
    snake = evolve_snake(snake, I, B, step_size);
    cla, imagesc(I)
    plot(snake([1:end,1], 2), snake([1:end, 1], 1), 'r', 'LineWidth', 2)
    title(['Iteration ', num2str(i)]), drawnow
end