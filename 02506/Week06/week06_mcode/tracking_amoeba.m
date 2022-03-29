clear
close all
addpath('functions')

%% setting
file_name = '../../../../Data/week6/crawling_amoeba.mov';
nr_points = 100;
alpha = 0.01;
beta = 0.01;
step_size = 10;
center = [120,200];
radius = 40;

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
    G(:,:,i) = double(rgb2gray(frame2im(M(i))))/255;
end

%% initialization
g = G(:,:,1); % image we operate on
B = regularization_matrix(nr_points,alpha,beta);
snake = make_circular_snake(center,radius,nr_points);

figure
imagesc(g), axis image, colormap gray
hold on, plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
drawnow

for i=1:100
    snake = evolve_snake(snake, g, B, step_size);
    cla, imagesc(g)
    plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
    title(['initialization, iter ', num2str(i)]), drawnow
end

%% tracking
for i=1:1/3:300%length(M) % non-integer steps for multiple evolutions per frame
    g = G(:,:,floor(i));
    snake = evolve_snake(snake, g, B, step_size);
    cla, imagesc(g)
    plot(snake([1:end,1],2),snake([1:end,1],1),'r','LineWidth',2)
    title(['tracking, frame ', num2str(floor(i))]), drawnow
end