import numpy as np

# Question 1
print('Question 1')

p = np.asarray([[1/8, 0, 1/8],[0, 1/2, 0],[1/8, 0, 1/8]])

# a)
print('\ta)')
py = np.sum(p,0)
print('\t\tP(Y) = '+str(py))
Hy = -sum(py*np.log2(py))
print('\t\tH(Y) = %.2f'% Hy)

# b)
print('\tb)')
P_temp = np.asarray([1/8,1/8,1/2,1/8,1/8])
Hxy = -np.sum(P_temp*np.log2(P_temp))
print('\t\tH(X,Y) = %.2f'%Hxy)

# c)
print('\tc)')
Hx = Hy
Hy_x = Hxy-Hx
print('\t\tH(X|Y) = %.2f'%Hy_x)

# d)
print('\td)')
Ixy = Hy-Hy_x
print('\t\tI(X;Y) = %.2f'%Ixy)

# Question 2
print('Question 2')
print('See test paper for Answers')

# Question 3
print('Question 3')
print('\tSee test paper for proof')

# Question 4
print('Question 4')
p =[.1, .4, .2, .25, .05]

# Part a
print('\tPart a.  Shannon Code')
for pi in p:
	print('\t\t%.2f | %.2f | %d' %(pi, -np.log2(pi), np.ceil(-np.log2(pi))))

print('\n\t\tE[l] = %.2f'%sum(p*np.ceil(-np.log2(p))))

# part b
print('\tPart b.  Huffman Code')
l = [4,1,3,2,4]
print('\t\tE[l] = %.2f'%sum(np.asarray(p)*np.asarray(l)))
# part c
print('\tPart c. Shannon-Fano-Elias')
def dec2bin(x):
	output_sequence = []
	for i in range(6):
		temp = int(x>=2**(-i-1))
		x -= temp * 2 ** (-i - 1)
		output_sequence.append(temp)
	return output_sequence

cmf = [0]
midpoints = []
for p_temp in p:
	cmf.append(cmf[-1] +p_temp )
	mid = np.mean([cmf[-1],cmf[-2]])

	print('\t\t'+str(dec2bin(mid)))
	midpoints.append(mid)
#print(midpoints)


# d
print('\tPart D: Comparison')
H = -sum(p*np.log2(p))
print('\t\t%.2f'%H)

# Question 5
print('\n Question 5')

# a)
print('\ta)')
r = np.asarray([1/2, 3/8, 1/8])
c = np.log2(3) - sum(-r*np.log2(r))
print('\t\tTrue %.2f'%c)
# b)
print('\tb)')
print('\t\tFalse %.2f'%np.log2(3))
# c)
print('\tc)')
print('\t\tTrue')
# d)
print('\td)')
print('\t\tFalse')
# e)
print('\te)')
print('\t\tFalse')
