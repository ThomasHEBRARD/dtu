%% Scale space exercise.
% Anders Dahl, abda@dtu.dk

% Data - change path to where you store the data
data_path = '../../../../Data/week2/';

% Computing Gaussian and its second order derivative

% Script for Gaussian to third order
t = 10;
s = sqrt(t);
x = -ceil(s*5):ceil(s*5);
g = exp(-x.^2/(2*s^2));
g = g/sum(g);
dg = -x/(s^2).*g;
ddg = -g/(s^2) - x/(s^2).*dg;
dddg = -dg/(s^2) - dg/(s^2) - x/(s^2).*ddg;

% Visualziation
figure
plot(g)
hold on
plot(dg)
plot(ddg)
plot(dddg)

%% Put the computation into a function

t = 325;
[g, dg, ddg, dddg] = getGaussDerivative(t);

figure
plot(g)
hold on
plot(dg)
plot(ddg)
plot(dddg)

im = double(imread([data_path 'test_blob_uniform.png']));

Lg = imfilter(imfilter(im, g, 'replicate'), g', 'replicate');

figure
imagesc(Lg)
axis image, colormap gray

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Detecting blobs on one scale

im = double(imread([data_path 'test_blob_uniform.png']));

Lxx = imfilter(imfilter(im, ddg, 'replicate'), g', 'replicate');
Lyy = imfilter(imfilter(im, ddg', 'replicate'), g, 'replicate');

L_blob = t*(Lxx + Lyy);

% show blob response
figure
imagesc(L_blob), axis image, colormap gray
%% Detect the blobs and draw a circle around each blob

% find regional maximum in laplacian
magnitudeThres = 50;

imregmax = imregionalmax(L_blob);
[rP, cP] = find(imregmax == 1 & L_blob > magnitudeThres);

imregmin = imregionalmin(L_blob);
[rN, cN] = find(imregmin == 1 & L_blob < -magnitudeThres);

% Show circles - draw lines at 202 sampling points
theta = [0:pi/100:2*pi, 0];
circ = [cos(theta); sin(theta)]';
nCirc = size(circ,1);

nPos = size(rP,1);
nNeg = size(rN,1);

figure
imagesc(im)
axis image
colormap gray
hold on
plot(cP, rP, '.r')
plot(sqrt(2*t)*circ(:,1)*ones(1,nPos) + ones(nCirc,1)*(cP'), sqrt(2*t)*circ(:,2)*ones(1,nPos) + ones(nCirc,1)*(rP'), 'r-', 'LineWidth', 2)
plot(cN, rN, '.b')
plot(sqrt(2*t)*circ(:,1)*ones(1,nNeg) + ones(nCirc,1)*(cN'), sqrt(2*t)*circ(:,2)*ones(1,nNeg) + ones(nCirc,1)*(rN'), 'b-', 'LineWidth', 2)


%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Detecting blobs on multiple scales

im = double(imread([data_path 'test_blob_varying.png']));

t = 15;
[g, dg, ddg, dddg] = getGaussDerivative(t);

[r,c] = size(im);
n = 100;
L_blob_vol = zeros(r,c,n);
tStep = zeros(1,n);

Lg = im;
for i = 1:n
    tStep(i) = t*i;
    L_blob_vol(:,:,i) = t*i*(imfilter(imfilter(Lg, ddg, 'replicate'), g', 'replicate') + ...
        imfilter(imfilter(Lg, ddg', 'replicate'), g, 'replicate'));
    Lg = imfilter(imfilter(Lg, g, 'replicate'), g', 'replicate');
end

%% find maxima in scale-space
% Compute regional maxima and minima
thres = 40;
ct_vol_pos = imregionalmax(L_blob_vol);
ct_vol_neg = imregionalmin(L_blob_vol);

% function to get coordinates and scales
[coordPos, scalePos] = getCoordScaleStep(ct_vol_pos, L_blob_vol, thres, tStep');
[coordNeg, scaleNeg] = getCoordScaleStep(ct_vol_neg, -L_blob_vol, thres, tStep');

% circles for plotting
circCoordsPos = getCircles(coordPos, scalePos);
circCoordsNeg = getCircles(coordNeg, scaleNeg);

% plot results
figure
imagesc(im), axis image, colormap gray
hold on
plot(coordPos(:,2), coordPos(:,1), '.r')
plot(circCoordsPos(:,:,2), circCoordsPos(:,:,1), 'r-', 'LineWidth', 2);
plot(coordNeg(:,2), coordNeg(:,1), '.b')
plot(circCoordsNeg(:,:,2), circCoordsNeg(:,:,1), 'b-', 'LineWidth', 2);

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Detecting blobs in real data

% diameter interval and steps
d = 10:.4:24;
tStep = sqrt(0.5)*((d/2).^2); % convert to scale

% read image and take out a small part
im = double(imread([data_path 'SEM.png']));
im = im(201:500,201:500);

figure
imagesc(im), axis image, colormap gray
%% Compute scale space

[r,c] = size(im);
n = size(d,2);
L_blob_vol = zeros(r,c,n);

for i = 1:n
    [g,~,ddg] = getGaussDerivative(tStep(i));
    L_blob_vol(:,:,i) = tStep(i)*(imfilter(imfilter(im, ddg, 'replicate'), g', 'replicate') + ...
        imfilter(imfilter(im, ddg', 'replicate'), g, 'replicate'));
end

%% Find maxima in scale space

% find local minima (no maxima since this is bright blobs)
ct_vol_neg = imregionalmin(L_blob_vol);

% threshold the undesired blobs
thres = 30;
[coordNeg, scaleNeg] = getCoordScaleStep(ct_vol_neg, -L_blob_vol, thres, tStep');

% get the circles to plot
circCoordsNeg = getCircles(coordNeg, scaleNeg);

% show the result
figure
imagesc(im), colormap gray, axis image
hold on
plot(coordNeg(:,2), coordNeg(:,1), '.r')
plot(circCoordsNeg(:,:,2), circCoordsNeg(:,:,1), 'r-', 'LineWidth', 1.2);

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Localize blobs

% Example low resolution lab X-ray CT
im = double(imread([data_path 'CT_lab_low_res.png']))/255;

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [3,6];
stepSize = 0.05;

% Parameter for Gaussian to detect center point
tCenter = 2;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 5;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');



%% Example medium resolution lab X-ray CT
im = double(imread([data_path 'CT_lab_med_res.png']))/255;

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [7,15];
stepSize = 0.15;

% Parameter for Gaussian to detect center point
tCenter = 4;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 8;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');


%% Example high resolution lab X-ray CT
im = double(imread([data_path 'CT_lab_high_res.png']))/255;

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [10,25];
stepSize = 0.3;

% Parameter for Gaussian to detect center point
tCenter = 20;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 8;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');


%% SEM image example

% Fibre experiment

% Image to analyse
im = double(imread([data_path 'SEM.png']));
im = im(1:650,:);

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [12,24];
stepSize = 0.3;

% Parameter for Gaussian to detect center point
tCenter = 8;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 8;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');


%% Synchrotron image example

% Fibre experiment

% Image to analyse
im = double(imread([data_path 'CT_synchrotron.png']));
im = im(701:1200,701:1200);

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [7,20];
stepSize = 0.1;

% Parameter for Gaussian to detect center point
tCenter = 12;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 4;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');

%% Optical image example

% Fibre experiment

% Image to analyse
im = double(imread([data_path 'Optical.png']));

figure
imagesc(im)
colormap gray, axis image

%% Set parameters

% Radius limit
diameterLimit = [10,15];
stepSize = 0.33;

% Parameter for Gaussian to detect center point
tCenter = 8;

% Parameter for finding maxima over Laplacian in scale-space
thresMagnitude = 10;

% Detect fibres
[coord, scale] = detectFibres(im, diameterLimit, stepSize, tCenter, thresMagnitude);

% Plot detected fibres
circCoords = getCircles(coord, scale);

% Show the resulting fibre detection
figure
imagesc(im), colormap gray, axis image
hold on
plot(coord(:,2), coord(:,1), '.r')
plot(circCoords(:,:,2), circCoords(:,:,1), 'r-');
























