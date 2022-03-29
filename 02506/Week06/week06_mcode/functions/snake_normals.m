function N = snake_normals(C)
% normals for a closed snake
% Author: vand@dtu.dk

X = C([end,1:end,1],:); % closed snake
dX = X(1:end-1,:)-X(2:end,:); % dX
Ne = normalize([dX(:,2),-dX(:,1)]); % edge normals orthogonal to dX
N = normalize(Ne(1:end-1,:) + Ne(2:end,:)); % vertices normals

function n = normalize(n)
d = sum(n.^2,2).^0.5;
nonzero = d~=0;
n(nonzero,:) = n(nonzero,:)./d(nonzero,[1 1]);


