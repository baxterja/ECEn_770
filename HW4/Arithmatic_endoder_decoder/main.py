import numpy as np

#Precompute Tables
alphabet = list('ABVSER!')
probabilities = [.15, .08, .02, .2, .29, .18, .08]
cmf = [0]
index_look_up = {}
for i, symbol in enumerate(alphabet):
	index_look_up[symbol] = i
	cmf.append(sum(probabilities[0:i+1]))


#Convert a decimal to 16bit binary representation (0 fills the end if fewer than 16 bits are needed)
def decimal_2_fixed_point(x, width):
	length = int(np.ceil(-np.log2(width)))+1
	output_sequence = []

	#compute binary representation
	for i in range(length):
		temp = int(x>=2**(-i-1))
		x -= temp * 2 ** (-i - 1)
		output_sequence.append(temp)
	#zero pad
	for i in range(length,16):
		output_sequence.append(0)
	return output_sequence

#Convert a binary to a decimal representation
def bin_2_dec(symbol):
	output = 0
	for i, v in enumerate(symbol):
		output += int(v=='1')*2**(-i-1)
	return output


#finds the new start and stop position of the encoding if the given symbol were to be encoded
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

	#Iterate throught the symbols to encode
	for symbol in sequence:
		#Find the new potential start and stop position
		start_temp, stop_temp = get_symbol_encoding(symbol, start, stop)

		#if the new encoding results in to high of preciscion encode a ! instead
		if np.ceil(-np.log2((stop_temp-start_temp)*probabilities[-1]))>15:
			start, stop = get_symbol_encoding('!', start, stop)

			#Convert the midpoint to a binary representation
			partial_encoding = decimal_2_fixed_point((start+stop)/2,stop-start)

			#Append encoding for later printing
			encoded_sequence_decimal.append((start+stop)/2)
			encoded_sequence_16bit.append(partial_encoding)

			#Reset the  start and stop position
			start = 0
			stop = 1
			# Encode the symbol you were originally trying to encode before determint a '!' was necassary
			start_temp, stop_temp = get_symbol_encoding(symbol, start, stop)

		#Update Endpoints
		start = start_temp
		stop = stop_temp

	#Finish the transmission by encoding a '!'
	start, stop = get_symbol_encoding('!', start, stop)
	partial_encoding = decimal_2_fixed_point((start + stop) / 2, stop - start)
	encoded_sequence_decimal.append((start + stop) / 2)
	encoded_sequence_16bit.append(partial_encoding)
	return encoded_sequence_16bit, encoded_sequence_decimal


def decode(sequence):
	decoded_sequence = []

	#Iterate throught everything to be decoded
	for symbol in sequence:
		symbol = bin_2_dec(symbol)
		start = 0
		stop = 1
		temp_decoded_symbol = 'A'

		#While a '!' isn't found keep decoding without resetting endboints
		while temp_decoded_symbol != '!':
			probs = start +(stop-start)*np.asarray(cmf)

			#Find which symbols is associated with the given with a given probability
			i = 0
			while symbol>=probs[i]:
				i+=1

			#Update endpoints
			size = (stop - start)
			stop = start + size * cmf[i]
			start = start + size * cmf[i - 1]
			temp_decoded_symbol = alphabet[i-1]

			#Don't append the '!' symbol to the encoding
			if temp_decoded_symbol!= '!':
				decoded_sequence.append(temp_decoded_symbol)
	return decoded_sequence



#Encode the given sequence
encoded_sequence, encoded_sequence_decimal = encode(list('ASBVRAERBSESEEERARSAEREESS'))

#Print the encoding
for l,f in zip(encoded_sequence,encoded_sequence_decimal):
	print(''.join(str(e) for e in l)+'\t'+str(f))

#Decode and print the given encoding
encoded_sequence_HW = [list('001101100001010'),list('001111011101011')]
decoded_sequence = decode(encoded_sequence_HW)
print(''.join(decoded_sequence))

