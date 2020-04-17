syms p
A = [1-p p; p 1-p];
[V, D] = eig(A);
pretty(V)
pretty(D)
