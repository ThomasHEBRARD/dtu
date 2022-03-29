% Computing length of segmentation boundary, exercise 1.1.2

clear, close all

path = '../../../../Data/week1/fuel_cells/';

figure
for i = 1:3
    I = imread([path, 'fuel_cell_',num2str(i),'.tif']);
    L = boundary_length(I);
    subplot(1,3,i)
    imagesc(I), axis image
    title(['L=',num2str(L)])
end


function L = boundary_length(S)
lx = S(2:end,:)~=S(1:end-1,:);
ly = S(:,2:end)~=S(:,1:end-1);
L = sum(lx(:))+sum(ly(:));
end