clear
close all
addpath('functions')

%A)
a = (40+10*1)^2*pi

filename = '../../../../Data/week6/plusplus.png';
I = double(rgb2gray(imread(filename)))/255;

snake = make_circular_snake(size(I)/2, 180, 200);
in = poly2mask(snake(:,2), snake(:,1), size(I,1), size(I,2));

m(1) = sum(I(:).*~in(:))/sum(~in(:)); % mean out
m(2) = sum(I(:).*in(:))/sum(in(:)); % mean in

b = m(2)

J = m(uint8(in)+1);

e = (I-J).^2;
c = sum(e(:))

figure
subplot(1,3,1)
imagesc(I,[0,1]), axis image, colormap gray, hold on
plot(snake([1:end, 1], 2), snake([1:end, 1], 1), 'r', 'LineWidth', 2)
subplot(1,3,2)
imagesc(J,[0,1]), axis image, colormap gray, title(['mean in = ',num2str(b)])
subplot(1,3,3)
imagesc(e), axis image, colormap gray, title(['external energy = ',num2str(round(c))])

