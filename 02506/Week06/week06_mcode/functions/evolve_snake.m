function snake = evolve_snake(snake, I, B, step_size)
% EVOLVE_SNAKE   Single step of snake evolution

[X,Y] = meshgrid(1:size(I,2),1:size(I,1));
in = poly2mask(snake(:,2), snake(:,1), size(I,1), size(I,2));
m_in = sum(I(:).*in(:))/sum(in(:));
m_out = sum(I(:).*~in(:))/sum(~in(:));
force = 0.5*(m_in-m_out)*(2*interp2(X, Y, I, snake(:,2), snake(:,1))-(m_in+m_out));
snake = snake + step_size*force*[1,1].*snake_normals(snake); % external part
snake = B*snake; % internal part
snake = keep_snake_inside(distribute_points(remove_intersections(snake)),size(I));
