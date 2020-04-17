import numpy as np
import itertools
import scipy.misc as comb
import scipy.stats as stats
import matplotlib.pyplot as plt
import scipy.linalg as linalg
import time

def dec2bin(value,length = None):
	if length == None:
		length = np.ceil(np.log2(value+1))
	if value>= 2**length:
		print('ivalid Length for dec2bin')
	temp_list = []
	for i in range(int(length)-1,-1,-1):
		temp_list.append(int(value>=2**i))
		value-=2**i*int(value>=2**i)
	return temp_list

def get_input_sequence(num_bits, epsilon = .5):
	return (np.random.rand(1,int(num_bits))<epsilon).astype(int)

def get_RM_Generator_matrix(levels, length):
	if levels<=0 or levels>length:
		print('invalid inputs for get_RM_Generator_matrix')
	temp_list = []
	for i in range(2**length):
		temp_list.append(dec2bin(i,length))
	generator = np.ones([1,2**length])
	generator = np.vstack([generator,np.asarray(temp_list).T])

	level1_possibilities = np.arange(1,length+1)
	for l in range(2,levels+1):
		combinations = itertools.combinations(level1_possibilities,l)
		for c in combinations:
			temp_row = generator[c,:].all(axis=0).astype(int)
			generator = np.vstack([generator,temp_row])
	return generator

def encode_message(input_sequence, G):
	return (np.matmul(input_sequence,G)%2).astype(int)

def decode_message(r, H, dimension):
	R = (-1)**r
	t = np.matmul(R,H)
	ti = np.argmax(np.abs(t))

	decoded_sequence = dec2bin(ti, dimension)
	if t[0,ti]<0:
		decoded_sequence[0] = 1

	return decoded_sequence

for r,m in zip([1,1,2],[3,4,4]):
	G = get_RM_Generator_matrix(r,m)
	print('RM(%d,%d), Dimension: %d, Blocklength: %d, Rate: %f, dmin: %d' % (
	r, m, sum(comb.comb(m, np.arange(0, r + 1))), 2 ** m, sum(comb.comb(m, np.arange(0, r + 1))) / 2 ** m,
	2 ** (m - r)))
	print(G)
#
# print('\n')
# # USED FOR TESTING THE ENCODING/DECODING
# for r,m in zip([1,1],[3,4]):
# 	dimension = int(sum(comb.comb(m, np.arange(0, r + 1))))
# 	G = get_RM_Generator_matrix(r, m)
# 	H = linalg.hadamard(2 ** m)
#
#
# 	for i in range(10):
# 		input_sequence = get_input_sequence(dimension)
# 		print('Input Sequence: ' + str(input_sequence))
# 		encoded_message = encode_message(input_sequence, G)
# 		print('Encoding: '+str(encoded_message))
# 		error_pattern = get_input_sequence(max(encoded_message.shape),.15)
# 		print('Error Pattern:'+str(error_pattern))
# 		message_recieved = (encoded_message+error_pattern)%2
# 		decoded_message = decode_message(message_recieved,H,dimension)
# 		print('Decoded: '+str(decoded_message))
# 		if (np.atleast_2d(decoded_message)==input_sequence).all():
# 			print('SUCCESS')
# 		else:
# 			print('FAIL')


gamma_list = []
error_list = [[],[]]
theoretical_error_list = []
N = 500
Eb = 1


for gamma in range(0,10):
	#print(gamma)
	if gamma>7:
		N = 20

	R = 1

	N0 = Eb / (10**(gamma/10))

	p_uncorrected = stats.norm.sf(np.sqrt(2*Eb/N0))
	theoretical_error_list.append(p_uncorrected)

	for i, (r, m) in enumerate(zip([1, 1], [3, 4])):
		n = 2 ** m
		dimension = sum(comb.comb(m, np.arange(0, r + 1)))
		rate = dimension / n
		Ec = Eb * rate
		G = get_RM_Generator_matrix(r, m)
		H = linalg.hadamard(2 ** m)

		p = stats.norm.sf(np.sqrt(2 * Ec / N0))
		total_counter = 0
		misclassification_count = 0
		while misclassification_count<=N:
			total_counter+=dimension  # add 4 or 11 bits
			input_sequence = get_input_sequence(dimension)
			encoded_message = encode_message(input_sequence, G)
			error_pattern = get_input_sequence(max(encoded_message.shape),p)
			message_recieved = (encoded_message+error_pattern)%2
			decoded_message = decode_message(message_recieved,H,dimension)

			num_errors = np.sum(~(np.atleast_2d(decoded_message)==input_sequence))
			misclassification_count+= num_errors


		error = misclassification_count/total_counter
		error_list[i].append(error)

	gamma_list.append(gamma)

plt.semilogy(gamma_list,error_list[0],'b',label= 'RM(1,3)')
plt.semilogy(gamma_list,error_list[1],'g',label= 'RM(1,4)')
plt.semilogy(gamma_list, theoretical_error_list,'r', label='Theorectical Uncorrected')
plt.legend()

plt.xlabel('E_b/N_0(db)')
plt.ylabel('Probability of bit error')
plt.show()
