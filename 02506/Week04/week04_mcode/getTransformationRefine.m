function [R,t,s,idx] = getTransformationRefine(p,q)

[R,t,s] = getTransformation(p, q);

% Change the scale of hte points
p_t = s*R*p + t;

% Refine the match by removing outliers
d = sqrt(sum((q-p_t).^2));
med_d = median(d)*1.5;
idx = find(d < med_d);

p_id = p(:,idx);
q_id = q(:,idx);

[R,t,s] = getTransformation(p_id, q_id);

