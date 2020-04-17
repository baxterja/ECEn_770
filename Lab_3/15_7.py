import numpy as np

A = np.asarray([[1,1,1,0,0,1,1,0,0,1],
				[1,0,1,0,1,1,0,1,1,0],
				[0,0,1,1,1,0,1,0,1,1],
				[0,1,0,1,1,1,0,1,0,1],
				[1,1,0,1,0,0,1,1,1,0]])

r = np.asarray([1,1,0,0,0,1,0,1,1,1])

Z = np.sum(A*r,axis=1)%2
V = np.matmul(Z,A)
print(Z)
print(V)