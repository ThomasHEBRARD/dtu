clear, close all
addpath GraphCut functions

I = [7,1,2,2,4,1;
     6,6,5,4,5,1;
     5,2,6,4,4,2;
     1,5,7,2,2,6;
     2,4,3,6,7,7];
 
%% part a) and b)
r = sum(I,2);
a = r(3)
b = min(r)
 
%% part c)
C = permute(I,[2,3,1]); % making sure that up is the third dimension
s = grid_cut(C, [], 2, 0);

figure
imagesc(I), hold on
plot(1:size(I,2),permute(s,[1,3,2]),'r','LineWidth',2)
c = sum(I(sub2ind(size(I),s',1:size(I,2))))
title(['cost=',num2str(c)])

%% JUST CHECKING FOR THE DIFFERENT VALUES OF DELTA
figure
for i=0:4
    subplot(2,3,i+1)
    imagesc(I), hold on
    s = grid_cut(C, [], i, 0);
    cost = sum(I(sub2ind(size(I),s',1:size(I,2))));
    plot(1:size(I,2),permute(s,[1,3,2]),'r','LineWidth',2)
    title(['delta=', num2str(i),', cost=',num2str(cost)])
end