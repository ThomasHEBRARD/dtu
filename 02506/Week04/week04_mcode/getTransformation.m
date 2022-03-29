function [R, t, s] = getTransformation(p,q)
% Computes the rotation, R, translation, t, and scale, s, of transforming
% point set p to q, such that sum_i(||s*R*p_i + t - q_i||).
% function: [R, t, s] = getTransformation(p,q)
% 

% Mean of the two point sets
mean_p = mean(p,2);
mean_q = mean(q,2);

% Eucledian distance to mean point
d_q = sqrt(sum((q-mean_q).^2));
d_p = sqrt(sum((p-mean_p).^2));

% Scale
s = d_q/d_p;

% Covarince matrix
H = (q-mean_q)*(p-mean_p)';

% SVD
[u,~,v] = svd(H);

% Rotation matrix
R = u*v;
R = u*[1,0;0,sign(det(R))]*v;

% Translation
t = mean_q - s*R*mean_p;

end