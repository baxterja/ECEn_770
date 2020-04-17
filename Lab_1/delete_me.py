from scipy.special import comb
def P(p,l,j):
	n =6
	ans =0
	for r in range(l+1):
		ans+=comb(j,l-r)*comb(n-j,r)*p**(j-l+2*r)*(1-p)**(n+l-j-2*r)
	return ans

prob = 0
for A,j in zip([4,3],[3,4]):
	prob_temp = 0
	for l in range(2):
		prob_temp+=P(.01,l,j)
	prob+=A*prob_temp

p_temp = 0
for j in range(2):
	prob_temp+=comb(6,j)*.01**j*(1-.01)**(6-j)

print(1-prob_temp-prob)