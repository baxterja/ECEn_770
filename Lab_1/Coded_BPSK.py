import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# BPSK
Ec = 1
n = 7
k = 4
R = k/n

if n-k == 3:
	H = np.asarray([[1,0,0,1,1,0,1],
					[0,1,0,1,0,1,1],
					[0,0,1,0,1,1,1]])
elif n-k ==4:
	H = np.asarray([[1,0,0,0,1,1,0,1,1,0,1,0,1,0,1],
					[0,1,0,0,1,0,1,1,0,1,1,0,0,1,1],
					[0,0,1,0,0,1,1,1,0,0,0,1,1,1,1],
					[0,0,0,1,0,0,0,0,1,1,1,1,1,1,1]])
else:
	H = None
gamma_list = []
error_list = []
theoretical_error_list = []
N = 100
for gamma in range(0,11):
	print(gamma)
	if gamma>7:
		N = 20
	N0 = Ec / (R*10**(gamma/10))
	Eb = Ec/R
	variance = N0/2
	p = stats.norm.sf(np.sqrt(2*Ec/N0))
	p_uncorrected = stats.norm.sf(np.sqrt(2*Eb/N0))
	theoretical_error_list.append(p_uncorrected)

	total_counter = 0
	misclassification_count = 0

	while misclassification_count<=N:
		r = (np.random.rand(n)<p).astype(int) #generate signal 7 or 15 long.  flip 1/p of them
		total_counter+=k  # add 4 or 11 bits
		s = r.dot(H.T) #find the syndrome

		if not sum(s)== 0:
			temp = (s==H.T).all(axis=1).astype(int)#find which bit was flipped
			r = (r + temp)%2 #flipped the predicted flipped bit

		misclassification_count+= sum(r[-k:]) #add the total number of non-zero recieved decoded bits.


	error = misclassification_count/total_counter

	gamma_list.append(gamma)
	error_list.append(error)
plt.semilogy(gamma_list,error_list,'b',label= 'Hamming Correction')
plt.semilogy(gamma_list, theoretical_error_list,'b--', label='Theorectical Uncorrected')
plt.legend()

plt.xlabel('E_b/N_0_(db)')
plt.ylabel('Probability of bit error')
plt.show()

# 4)The larger N is the more accurate the estimated to the theoretical.  However for larger gammas It takes to long
#   To run the simulation for large N.  Thus it get less acurate since I decrease N.  A theoretical model is very
#   Helpful when you want to estimate error rates for really large signal to noise ratio since it allows you not to wait
#   forever for your simulation to run.

# 5)The larger the skew the lower the error rate.  This makes since if p0 = 0 or 1 then the probability of error = 0.
#   However there is a trade off because the larger the skew of the bits the less information it carries.


