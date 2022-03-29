% optional exercise 1.1.4

path = '../../../../Data/week1/';
I = imread([path, 'fibres_xcth.png']);

I = double(I)/(2^16-1);
I = I(301:700,301:700);
v = total_variation(I);
sigma = 5;
truncate = 3*2*sigma+1; % truncating size of gaussian
Is = imfilter(I,fspecial('gaussian',truncate*[1,1],sigma),'replicate');
vs = total_variation(Is);

figure 
subplot(121)
imagesc(I), colormap gray, axis image
title(['total variation is ', num2str(v)])
subplot(122)
imagesc(Is), colormap gray, axis image
title(['total variation is ', num2str(vs)])

function v = total_variation(I)

[dx,dy] = gradient(double(I));
v = sum(abs(dx(:)))+sum(abs(dy(:)));

end