import Viterbi_class
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

G = np.asarray([[[1,0,1],[1,1,1]]])
encoder = Viterbi_class.Viterbi_encoder(G)
trellis_dict = [[0,2],
				[0,2],
				[1,3],
				[1,3]]


N = 100
Eb = 2
Ec = 1
theoretical_error_list = []
hard_decision_error_list = []
soft_decision_error_list = []


for gamma in range(0,11):
	print(gamma)
	N0 = Eb / (10 ** (gamma / 10))
	p_uncorrected = stats.norm.sf(np.sqrt(2 * Eb / N0))
	theoretical_error_list.append(p_uncorrected)

	input_buffer = []
	for i in range(21):
		input_buffer.append(0)
	input_buffer_location = 0

	decoder_hard = Viterbi_class.Viterbi_decoder(G, trellis_dict)
	decoder_soft = Viterbi_class.Viterbi_decoder(G, trellis_dict, is_hard_encoder=False)

	soft_done = False
	hard_done = False
	if gamma>6:
		soft_done = True
	if gamma>8:
		hard_done = True

	soft_errors = 0
	hard_errors = 0
	total_count = 0

	SD = np.sqrt(N0/2)

	while not (hard_done and soft_done):
		encoder_input = np.random.randint(0,2)
		input_buffer[input_buffer_location] = encoder_input
		encoded_bits = encoder.encode(encoder_input)
		noise = SD*np.random.randn(2)
		encoded_bits = -(-1)**encoded_bits + noise#np.random.normal(0,SD,2)
		total_count+=1
		if not soft_done:
			decoded_soft = decoder_soft.decode(encoded_bits)
			soft_errors += not(decoded_soft==input_buffer[input_buffer_location-1])
			if soft_errors>N:
				print('\tSoft Done')
				soft_done=True
				soft_decision_error_list.append(soft_errors/(total_count-20))
		if not hard_done:
			decoded_hard = decoder_hard.decode(encoded_bits)
			hard_errors += not(decoded_hard == input_buffer[input_buffer_location-1])
			# print('%d %d'%(decoded_hard,input_buffer[input_buffer_location-1]))
			if hard_errors > N:
				print('\tHard Done')
				hard_done = True
				hard_decision_error_list.append(hard_errors / (total_count - 20))
		input_buffer_location-=1
		input_buffer_location%=21

plt.semilogy(np.arange(7), soft_decision_error_list, 'b', label='Soft Decisions')
plt.semilogy(np.arange(9), hard_decision_error_list, 'g', label='Hard Decisions')
plt.semilogy(np.arange(11), theoretical_error_list, 'r', label='Theorectical Uncorrected')
plt.legend()

plt.xlabel('E_b/N_0(db)')
plt.ylabel('Probability of bit error')
plt.show()

# for encoded_bits in [[1,1],[1,0],[1,0],[1,1],[1,1],[0,1],[0,0],[0,1],]:
# 	encoded_bits = -(-1)**np.asarray(encoded_bits)
# 	decoding = decoder_hard.decode(encoded_bits)

# input_buffer = []
# for i in range(21):
# 	input_buffer.append(0)
# input_buffer_location = 0
# hard_errors = 0
# for i in range(10):
# 	for encoder_input in [1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0]:
# 		input_buffer[input_buffer_location] = encoder_input
# 		encoded_bits = encoder.encode(encoder_input)
# 		encoded_bits = -(-1)**encoded_bits# + np.random.normal(0,SD,2)
#
# 		decoded_hard = decoder_hard.decode(encoded_bits)
# 		hard_errors += not(decoded_hard == input_buffer[input_buffer_location-1])
# 		print('%d %d'%(decoded_hard,input_buffer[input_buffer_location-1]))
# 		input_buffer_location-=1
# 		input_buffer_location%=21
#
# print(hard_errors)



