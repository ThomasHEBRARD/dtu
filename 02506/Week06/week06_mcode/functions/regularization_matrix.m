function [B,A] = regularization_matrix(N,alpha,beta)
% B is an NxN matrix for imposing elasticity and rigidity to snakes
% alpha is weigth for second derivative (elasticity)
% beta is weigth for (-)fourth derivative (rigidity)
% vand@dtu.dk

r = zeros(1,N);
r(1:3) = alpha*[-2 1 0]/4 + beta*[-6 4 -1];
r(end-1:end) = alpha*[0 1]/4 + beta*[-1 4];
A = toeplitz(r);
B = (eye(N)-A)^-1;