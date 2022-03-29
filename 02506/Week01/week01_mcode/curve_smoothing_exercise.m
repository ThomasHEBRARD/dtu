% Curve smoothing, exercise 1.1.3

clear
close all

path = '../../../../Data/week1/curves/';

X_smooth = dlmread([path, 'dino.txt']);
X_noisy = dlmread([path, 'dino_noisy.txt']);
N = size(X_noisy,1);

figure, hold on
plot(X_smooth([1:end,1],1),X_smooth([1:end,1],2),'g')
plot(X_noisy([1:end,1],1),X_noisy([1:end,1],2),'r')
legend('ground truth','noisy','Location','N'), axis image

%%
% Explicit smoothing, comparing small lambda, big lambda and many iterations.
% Instead of looping, iterations implemented as matrix power.

lambda_small = 0.25;
lambda_big = 1;
nr_iters = 100;

off_diag = diag(ones(N-1,1),-1) + diag(1,N-1);
L = -2*diag(ones(N,1)) + off_diag + off_diag';
smoothed_small = (lambda_small*L+eye(N))*X_noisy;
smoothed_big = (lambda_big*L+eye(N))*X_noisy;
smoothed_many = (lambda_small*L+eye(N))^nr_iters*X_noisy;

figure, hold on
plot(smoothed_small([1:end,1],1),smoothed_small([1:end,1],2),'r')
plot(smoothed_big([1:end,1],1),smoothed_big([1:end,1],2),'k')
plot(smoothed_many([1:end,1],1),smoothed_many([1:end,1],2),'c')
legend(['explicit 1 iteration lambda ',num2str(lambda_small)],...
    ['explicit 1 iteration lambda ',num2str(lambda_big)],...
    ['explicit ',num2str(nr_iters), ' iterations lambda ', num2str(lambda_small)],'Location','N'), axis image


%%
% Implicit smoothing with both alpha and beta

alpha = 10;
beta = 10;

smoothed_a = regularization_matrix(N,alpha,0)*X_noisy;
smoothed_b = regularization_matrix(N,0,beta)*X_noisy;

figure, hold on
plot(smoothed_a([1:end,1],1),smoothed_a([1:end,1],2),'b')
plot(smoothed_b([1:end,1],1),smoothed_b([1:end,1],2),'m')
legend(['implicit alpha ', num2str(alpha)],['implicit beta ', num2str(beta)],'Location','N'), axis image


%% SOLVING QUIZ 2021
N = size(X_noisy,1);
off_diag = diag(ones(N-1,1),-1) + diag(1,N-1);
L = -2*diag(ones(N,1)) + off_diag + off_diag';
X_solution = (0.25*L+eye(N))*X_noisy;

figure
plot(X_noisy(:,1),X_noisy(:,2), 'r')
hold on
plot(X_solution(:,1),X_solution(:,2),'b--')
title(['noisy:' num2str(curve_length(X_noisy),'%.5g'),', smoothed:',...
    num2str(curve_length(X_solution), '%.5g')])

%%

function d = curve_length(X)
    d = X-X([2:end,1],:);
    d = sum(d.^2, 2);
    d = sum(sqrt(d));
end

function B = regularization_matrix(N,alpha,beta)
% B is an NxN matrix for imposing elasticity and rigidity to snakes
% alpha is weigth for second derivative (elasticity)
% beta is weigth for (-)fourth derivative (rigidity)

r = zeros(1,N);
r(1:3) = alpha*[-2 1 0] + beta*[-6 4 -1];
r(end-1:end) = alpha*[0 1] + beta*[-1 4];
A = toeplitz(r);
B = (eye(N)-A)^-1;

end
