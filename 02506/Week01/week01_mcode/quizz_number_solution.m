
I_noisy = double(imread('../../../../Data/week1/noisy_number.png'));
sigma = 15;
filter = fspecial('gaussian',(6*sigma+1)*[1,1],sigma);
I_smoothed = imfilter(I_noisy,filter,'circular');
figure, imagesc(I_smoothed), axis equal, colormap gray