function [V1,V2] = segmentation_energy(S, I, mu, beta)

% likelihood energy
V1 = sum(sum((mu(S)-I).^2));

% prior energy
V2x = S(:,2:end)~=S(:,1:end-1);
V2y = S(2:end,:)~=S(1:end-1,:);
V2 = beta*sum([V2x(:); V2y(:)]);



