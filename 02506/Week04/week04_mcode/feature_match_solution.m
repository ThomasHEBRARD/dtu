% Exercise on feature-based registration

% Create a random point set
% Set parameters for a random point set that is rotated and translated
n = 20; % number of random points
theta = 0.7*pi; % rotation angle
R_in = [cos(theta), -sin(theta); sin(theta), cos(theta)]; % rotation matrix
T_in = rand(2,1)*1.5; % translation vector (random)
s_in = 1.3; % scale

% Compute points
p = rand(2,n); % random point set
mean_p = mean(p,2); % man point

q = R_in*p + T_in; % transform the scaled points 
q = q + 0.05*rand(2,n); % add noise to the image

% Show the result
figure()
plot([p(1,:); q(1,:)], [p(2,:); q(2,:)], 'g', 'LineWidth', 2)
hold on
plot(p(1,:), p(2,:), 'r.', 'MarkerSize', 25)
plot(q(1,:), q(2,:), 'b.', 'MarkerSize', 25)
axis equal off

%% Recover parameters

% Find scale
mean_q = mean(q,2);
d_q = sqrt(sum((q-mean_q).^2));
d_p = sqrt(sum((p-mean_p).^2));
s = d_q/d_p;

% Find covariance matrix
C = (q-mean_q)*(p-mean_p)';

[u,ss,v] = svd(C);

R = u*v;
R = u*[1,0;0,sign(det(R))]*v;

T = mean_q - s*R*mean_p;



%% Plot the transformed points

q_new = s*R*p + T; % transform the scaled points 

% Show the result
figure()
plot([q_new(1,:); q(1,:)], [q_new(2,:); q(2,:)], 'g', 'LineWidth', 2)
hold on
plot(q_new(1,:), q_new(2,:), 'r.', 'MarkerSize', 25)
plot(q(1,:), q(2,:), 'b.', 'MarkerSize', 25)
axis equal off



%% Compute parameters and transform points based on the function

[R, t, s] = getTransformation(p,q); % Compute the transformation parameters from the function

q_new = s*R*p + t; % transform the scaled points 

% Show the result
figure()
plot([q_new(1,:); q(1,:)], [q_new(2,:); q(2,:)], 'g', 'LineWidth', 2)
hold on
plot(q_new(1,:), q_new(2,:), 'r.', 'MarkerSize', 25)
plot(q(1,:), q(2,:), 'b.', 'MarkerSize', 25)
axis equal off

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Get SFIT features and match them

% Change path to vlfeat to where you have put it
addpath /Users/abda/Documents/Teaching/02506/code/vlfeat-0.9.21/toolbox 
vl_setup

% Path to data - change to where you have put the data
data_path = '../../../../Data/week4/';

%% Compute SIFT features in one image and plot the points

im = single(imread([data_path 'CT_lab_high_res.png'])); % read image

% Show image
figure
imagesc(im), colormap gray, axis image 

% Compute SIFT
[f,d] = vl_sift(im);

% Show 500 random features
perm = randperm(size(f,2)) ;
sel = perm(1:500) ;
h1 = vl_plotframe(f(:,sel)) ;
h2 = vl_plotframe(f(:,sel)) ;
set(h1,'color','y','linewidth',3) ;
set(h2,'color','r','linewidth',3) ;


%% Compute SIFT features and match an image and its scaled version
angle = 120;
scale_factor = 0.5;

% Transform image
im_transform = imrotate(imresize(im, scale_factor), angle);

figure
imagesc(im_transform)
%%

% Compute SIFT features
[fa, da] = vl_sift(im) ;
[fb, db] = vl_sift(im_transform) ;

% Match features
[matches, scores] = vl_ubcmatch(da, db) ;

% Construct a total image
[rh,ch]=size(im);
[rm,cm]=size(im_transform);

im_tot = zeros(max(rh,rm), ch+cm);
im_tot(1:rh, 1:ch) = im;
im_tot(1:rm, 1+ch:end) = im_transform;

% Show the matched images
figure
imagesc(im_tot), axis image, colormap gray
hold on
plot(fa(1,matches(1,:)),fa(2,matches(1,:)),'b.', 'MarkerSize', 10)
plot(fb(1,matches(2,:))+ch,fb(2,matches(2,:)),'g.', 'MarkerSize', 10)
plot([fa(1,matches(1,:));fb(1,matches(2,:))+ch],[fa(2,matches(1,:));fb(2,matches(2,:))], 'r', 'LineWidth', 1)




%% Compute SIFT features and match between two images of the s

% Read two images
im_high = single(imread([data_path 'CT_lab_high_res.png']));
im_med = single(imread([data_path 'CT_lab_med_res.png']));

% Compute SIFT features
[fa, da] = vl_sift(im_high) ;
[fb, db] = vl_sift(im_med) ;

% Match features
[matches, scores] = vl_ubcmatch(da, db) ;

% Construct a total image
[rh,ch]=size(im_high);
[rm,cm]=size(im_med);

im_tot = zeros(max(rh,rm), ch+cm);
im_tot(1:rh, 1:ch) = im_high;
im_tot(1:rm, 1+ch:end) = im_med;

% Show the matched images
figure
imagesc(im_tot), axis image, colormap gray
hold on
plot(fa(1,matches(1,:)),fa(2,matches(1,:)),'b.', 'MarkerSize', 10)
plot(fb(1,matches(2,:))+ch,fb(2,matches(2,:)),'g.', 'MarkerSize', 10)
plot([fa(1,matches(1,:));fb(1,matches(2,:))+ch],[fa(2,matches(1,:));fb(2,matches(2,:))], 'r', 'LineWidth', 1)

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Transform matched features

% two corresponding sets of features
pa = fa(1:2,matches(1,:));
pb = fb(1:2,matches(2,:));

% Compute the transformation
[R,t,s] = getTransformation(pa,pb);

% Apply the transformation
pa_t = s*R*pa + t;

figure
imagesc(im_med), axis equal, colormap gray
hold on
plot([pa_t(1,:); pb(1,:)], [pa_t(2,:); pb(2,:)], 'g', 'LineWidth', 2)
plot(pa_t(1,:), pa_t(2,:), 'r.', 'MarkerSize', 10)
plot(pb(1,:), pb(2,:), 'b.', 'MarkerSize', 10)

%% Refined transformation

[R,t,s,idx] = getTransformationRefine(pa,pb);
pa_r = pa(:,idx);
pb_r = pb(:,idx);

pa_t = s*R*pa_r + t;

figure
imagesc(im_med), axis equal, colormap gray
hold on
plot([pa_t(1,:); pb_r(1,:)], [pa_t(2,:); pb_r(2,:)], 'g', 'LineWidth', 2)
plot(pa_t(1,:), pa_t(2,:), 'r.', 'MarkerSize', 10)
plot(pb_r(1,:), pb_r(2,:), 'b.', 'MarkerSize', 10)


