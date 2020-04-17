%% Poblem 1

Pxy = [1/8 0 1/8;...
       0  1/2  0;...
       1/8 0 1/8];
% A
Py = sum(Pxy)
Hy = -sum(Py.*log2(Py))

% B
temp = [1/8 1/8 1/2 1/8 1/8];
Hxy = -sum(temp.*log2(temp))

%% Problem 4
p = [.1 .4 .2 .25 .05];
cdf

