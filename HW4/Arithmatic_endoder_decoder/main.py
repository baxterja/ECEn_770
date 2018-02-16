import numpy as np

alphabet = list('ABVSER!')
probabilities = [.15, .08, .02, .2, .29, .18, .08]
cmf = [0]
index_look_up = {}
for i, symbol in enumerate(alphabet):
	index_look_up[symbol] = i
	cmf.append(sum(probabilities[0:i+1]))


def decimal_2_fixed_point(x, width):
	length = int(np.ceil(-np.log2(width)))+1
	output_sequence = []
	for i in range(length):
		temp = int(x>=2**(-i-1))
		x -= temp * 2 ** (-i - 1)
		output_sequence.append(temp)
	for i in range(length,16):
		output_sequence.append(0)
	return output_sequence

def bin_2_dec(symbol):
	output = 0
	for i, v in enumerate(symbol):
		output += int(v=='1')*2**(-i-1)
	return output


def get_symbol_encoding(symbol, start, stop):
	i = index_look_up[symbol]
	new_start = start+(stop-start)*cmf[i]
	new_stop = start + (stop - start) * cmf[i+1]
	return new_start, new_stop

def encode(sequence):

	encoded_sequence_decimal = []
	encoded_sequence_16bit = []
	start = 0
	stop = 1
	current_length = 0
	for symbol in sequence:
		start_temp, stop_temp = get_symbol_encoding(symbol, start, stop)
		if np.ceil(-np.log2((stop_temp-start_temp)*probabilities[-1]))>15:
			start, stop = get_symbol_encoding('!', start, stop)
			partial_encoding = decimal_2_fixed_point((start+stop)/2,stop-start)
			encoded_sequence_decimal.append((start+stop)/2)
			encoded_sequence_16bit.append(partial_encoding)
			start = 0
			stop = 1
			start_temp, stop_temp = get_symbol_encoding(symbol, start, stop)
		start = start_temp
		stop = stop_temp
	start, stop = get_symbol_encoding('!', start, stop)
	partial_encoding = decimal_2_fixed_point((start + stop) / 2, stop - start)
	encoded_sequence_decimal.append((start + stop) / 2)
	encoded_sequence_16bit.append(partial_encoding)
	return encoded_sequence_16bit, encoded_sequence_decimal


def decode(sequence):
	start = 0
	stop = 1
	decoded_sequence = []
	for symbol in sequence:
		symbol = bin_2_dec(symbol)
		start = 0
		stop = 1
		temp_decoded_symbol = 'A'
		while temp_decoded_symbol != '!':
			probs = start +(stop-start)*np.asarray(cmf)
			i = 0
			while symbol>=probs[i]:
				i+=1
			size = (stop - start)
			stop = start + size * cmf[i]
			start = start + size * cmf[i - 1]
			temp_decoded_symbol = alphabet[i-1]
			if temp_decoded_symbol!= '!':
				decoded_sequence.append(temp_decoded_symbol)
	return decoded_sequence



encoded_sequence, encoded_sequence_decimal = encode(list('ASBVRAERBSESEEERARSAEREESS'))
for l,f in zip(encoded_sequence,encoded_sequence_decimal):
	print(''.join(str(e) for e in l)+'\t'+str(f))

encoded_sequence_HW = [list('001101100001010'),list('001111011101011')]


decoded_sequence = decode(encoded_sequence_HW)
print(''.join(decoded_sequence))

