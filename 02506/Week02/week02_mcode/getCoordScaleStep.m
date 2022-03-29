function [coord, scale] = getCoordScaleStep(ct_vol, L_blob, thres, tStep)
% Finds coordinates and scales from the output of the functions 
% imregionalmax or imregionalmin
% 
% Input:
%     ct_vol : volume wiht 1 in positions of regional max/min
%     L_blob : Laplacian response
%     thres : Threshold for laplacian response
%     tStep : value of t (variance) in each step
% 
% Output:
%    coord : n x 2 array of coordinates with row and column coordinates in each column.
%    scale : n x 1 array of scales t (variance of the Gaussian).
% 
% Anders B. Dahl, abda@dtu.dk
% 
    [r,c,l] = size(ct_vol);

    idx = find(ct_vol == 1);
    magnitude = L_blob(idx);
    idx = idx(magnitude>thres);

    scale = ceil(idx/(r*c));
    coordC = ceil((idx - (scale-1)*r*c)/r);
    coordR = idx - (scale-1)*r*c - (coordC-1)*r;
    coord = [coordR, coordC];
    scale = tStep(scale);
end