import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.spatial.distance as distance
import cmath

# BPSK
Eb = 1

d_min = np.sqrt((1-Eb/np.sqrt(2))**2+(Eb/np.sqrt(2))**2)

codes= {0: [0, 0, 0],
		1: [0, 0, 1],
		2: [0, 1, 1],
		3: [0, 1, 0],
		4: [1, 1, 0],
		5: [1, 1, 1],
		6: [1, 0, 1],
		7: [1, 0, 0]}

gamma_list = []
symbol_error_list = []
bit_error_list = []
theoretical_error_list = []
N = 1000
for gamma in range(0,15):

	N0 = Eb / (10 ** (gamma/10))
	variance = N0/2

	total_counter = 0
	misclassification_count = 0
	bit_misclassification_count = 0

	while misclassification_count<=N:
		signal_sent = np.random.randint(0,8)
		if signal_sent == 8:
			print('warning')
		r_x = Eb*np.cos(signal_sent*2*np.pi/8) + np.random.normal(0,np.sqrt(variance))
		r_y = Eb*np.sin(signal_sent * 2 * np.pi / 8) + np.random.normal(0, np.sqrt(variance))

		recieved_angle = np.arctan2(r_y,r_x)
		if recieved_angle<0:
			recieved_angle += 2*np.pi

		recieved_signal = np.round(recieved_angle/(np.pi/4))%8

		total_counter+=1
		if not recieved_signal == signal_sent:
			misclassification_count+=1
			bit_misclassification_count += distance.hamming(codes[recieved_signal],codes[signal_sent])*len(codes[signal_sent])
	bit_error = bit_misclassification_count/total_counter
	error = misclassification_count/total_counter
	print('gamma = %f, P(e) = %f, P(b_e) = %f'%(gamma,error, bit_error))
	gamma_list.append(gamma)
	symbol_error_list.append(error)
	bit_error_list.append(bit_error)
	theoretical_error = 2*stats.norm.sf(d_min/(2*np.sqrt(variance)))
	theoretical_error_list.append(theoretical_error)
plt.semilogy(gamma_list,symbol_error_list,'b',label= 'Simulated Symbol Error')
plt.semilogy(gamma_list,theoretical_error_list,'b--',label= 'Theoretical Symbol Error bound')
plt.semilogy(gamma_list,bit_error_list,'r',label= 'Simulated bit Error')
plt.semilogy(gamma_list,theoretical_error_list,'r--',label= 'Theoretical bit Error bound')
plt.legend()

plt.xlabel('E_b/N_0_(db)')
plt.ylabel('Probability of bit error')
plt.show()




