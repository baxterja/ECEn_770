import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# BPSK
Eb = 1


for p0, c in zip([.5, .25, .1],['r', 'g', 'b']):
	gamma_list = []
	error_list = []
	theoretical_error_list = []
	N = 100
	for gamma in range(0,10):
		if gamma>7:
			N = 10
		N0 = Eb / (10 ** (gamma/10))
		variance = N0/2

		tau = variance/(2*np.sqrt(Eb))*np.log(p0/(1-p0))

		total_counter = 0
		misclassification_count = 0

		while misclassification_count<=N:
			signal = 2*int(np.random.rand()>p0)-1
			noise = np.random.normal(0,np.sqrt(variance))
			r = signal+noise
			total_counter+=1
			if not 2*int(r>tau)-1 == signal:
				misclassification_count+=1
		error = misclassification_count/total_counter
		print('P0 = %f, gamma = %f, P(error) = %f'%(p0,gamma,error))
		gamma_list.append(gamma)
		error_list.append(error)
		theoretical_error = stats.norm.sf((tau+np.sqrt(Eb))/np.sqrt(variance))*p0 + \
							stats.norm.sf((np.sqrt(Eb)-tau)/np.sqrt(variance))*(1-p0)
		theoretical_error_list.append(theoretical_error)
	plt.semilogy(gamma_list,error_list,c,label= 'p0 = %.2f'%p0)
	plt.semilogy(gamma_list, theoretical_error_list,c+'--', label='GT_p0 = %.2f' % p0)
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


