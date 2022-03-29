function S = keep_snake_inside(S,dim)
% constrains snake to image domain

S(:,1) = max(min(S(:,1), dim(1)), 1);
S(:,2) = max(min(S(:,2), dim(2)), 1);