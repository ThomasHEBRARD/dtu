function segmentation_histogram(I, S, edges)
%SEGMENTATION_HISTOGRAM Histogram for data and each segmentation label.
%
% h = label_histogram(V, S, bins)
%
% V is a data which is to be placed in bins
% S is some segmentation of the data, elements of S are in {1,...,K}
% bins is an optional vector specifying bins, just as in hist(data,bins)
%
% vand@dtu.dk, 2014

if nargin < 3
    edges = linspace(double(min(I(:))), double(max(I(:))));
end
if islogical(S)
    S = S + 1;
end
histogram(I(:), edges, 'EdgeColor', 'none', 'FaceColor', 'k') 
hold on
centers = 0.5*(edges(1:end-1) + edges(2:end));
for k = 1:max(S(:))
    plot(centers, (histcounts(I(S==k), edges)), 'LineWidth', 1.5)
end