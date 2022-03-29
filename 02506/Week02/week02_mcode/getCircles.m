function circCoords = getCircles(coord, scale)
% Comptue circle coordinages
% 
% Input:
%     coord : 2D array of coordinates.
%     scale : scale of individual blob (t).
% 
% Output:
%     circCoords : m x n x 2 coordinates of circle. m is the number of 
%                  sampling points on the circle, n is hte number of
%                  coordinates and the last dimension is the row, col
%                  coordinates.
% 
% Anders B. Dahl, abda@dtu.dk
% 

theta = [0:pi/100:2*pi, 0];
circ = [cos(theta); sin(theta)]';
nCirc = size(circ,1);

n = size(coord,1);

circCoords = zeros(nCirc, n, 2);
circCoords(:,:,1) = (ones(nCirc,1)*sqrt(2*scale')).*(circ(:,1)*ones(1,n)) + ones(nCirc,1)*(coord(:,1)');
circCoords(:,:,2) = (ones(nCirc,1)*sqrt(2*scale')).*(circ(:,2)*ones(1,n)) + ones(nCirc,1)*(coord(:,2)');



