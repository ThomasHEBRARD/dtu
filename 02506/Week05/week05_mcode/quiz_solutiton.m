clear
addpath GraphCut
addpath functions

I = [1,2,6,4,10,8; 4,1,3,5,9,6; 5,2,3,5,4,7];
mu = [2,5,10];
beta = 10;

%% A
U = [(I(:)-mu(1)).^2, (I(:)-mu(2)).^2, (I(:)-mu(3)).^2];
[~, S0] = min(U, [], 2);
S0 = reshape(S0, size(I));
prior_noisy = prior_energy(S0, beta);
disp(['prior_noisy ', num2str(prior_noisy)])

%% B
S = repmat([1,1,2,2,3,3],[3,1]);
likelihood_stripes = likelihood_energy(S, I, mu);
disp(['likelihood_stripes ', num2str(likelihood_stripes)])

%% C
S_best = multilabel_MRF(U, size(I), beta);
posterior_small = prior_energy(S_best, beta) + likelihood_energy(S_best, I, mu);
disp(['posterior_small ', num2str(posterior_small)])

%% ﻿another realization with the same posterior
S_test = repmat([1,1,2,2,2,2],[3,1]);
posterior_test = prior_energy(S_test, beta) + likelihood_energy(S_test, I, mu);
disp(['posterior_test ', num2str(posterior_test)])

function V2 = prior_energy(S, beta)
V2x = S(:,2:end)~=S(:,1:end-1);
V2y = S(2:end,:)~=S(1:end-1,:);
V2 = beta*sum([V2x(:); V2y(:)]);
end

function V1 = likelihood_energy(S, I, mu)
V1 = sum(sum((mu(S)-I).^2));
end