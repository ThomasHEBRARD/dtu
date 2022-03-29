clear
close all
addpath('functions')

%% setting
file_name = '../../../../Data/week6/echiniscus.mp4';
nr_points = 100;
alpha = 0.01;
beta = 0.01;
step_size = 10;
center = [120,200];
radius = 40;
start_frame = 75;

%% read movie data
v = VideoReader(file_name);
i = 1;
while hasFrame(v)
    M(i) = im2frame(readFrame(v));
    i = i+1;
end

%% process movie data
G = zeros(size(M(1).cdata, 1), size(M(1).cdata, 2), length(M));
for i=1:length(M)
    fr = double(frame2im(M(i)))/255;
    G(:,:,i) = (2*fr(:,:,3) - fr(:,:,2) - fr(:,:,1)+2)/4;
end

%% initialization
g = G(:,:,start_frame); % image we operate on
m = frame2im(M(start_frame)); % image we show
B = regularization_matrix(nr_points,alpha,beta);
snake = make_circular_snake(center,radius,nr_points);

figure
imagesc(m), axis image, colormap gray
hold on, plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
title(0), drawnow
for i=1:200
    snake = evolve_snake(snake, g, B, step_size);
    cla, imagesc(m)
    plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
    title(['initialization, iter ', num2str(i)]), drawnow
end

%% tracking
for i = start_frame + (1:1/3:500) % non-integer steps for multiple evolutions per frame
    g = G(:,:,floor(i));
    m = frame2im(M(floor(i)));
    snake = evolve_snake(snake, g, B, step_size);
    cla, imagesc(m)
    plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
    title(['tracking, frame ', num2str(floor(i))]), drawnow
end