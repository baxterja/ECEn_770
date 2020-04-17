import numpy as np

class Viterbi_encoder:
	def __init__(self, G):
		self.G = G
		self.in_size = G.shape[0]
		self.out_size = G.shape[1]
		self.state_size = G.shape[2]
		self.states = np.zeros([self.in_size,self.state_size])

		self.output = np.zeros(self.out_size)

	def add_input(self,inputs):
		self.states = np.roll(self.states,1)
		self.states[:,0] = inputs

	def update_current_output(self):
		for i in range(self.out_size):
			self.output[i]= int(np.sum(self.states*self.G[:,i,:])%2)

	def encode(self,input):
		self.add_input(input)
		self.update_current_output()
		return self.output


class Viterbi_decoder:
	def __init__(self, G, trellis_dict, decision_lag=20, is_hard_encoder= True):
		self.G = G
		self.trellis_dict = trellis_dict
		self.in_size = G.shape[0]
		self.out_size = G.shape[1]
		self.state_size = G.shape[2]
		self.NUM_STATES = 2**(self.state_size-1)
		self.trellis = np.zeros([self.NUM_STATES,decision_lag,2])
		self.decision_lag = decision_lag
		self.current_location = 0
		self.decoding = np.zeros(self.in_size)
		self.zeroone = np.asarray([[0,1]])
		self.pre_compute_cost = [[],[],[],[]]
		self.pre_compute_table = []
		self.get_pre_commpute_table()
		self.is_hard_encoder = is_hard_encoder


	# def get_pre_commpute_table(self):
	# 	for key, encoding in zip(range(4),[[0,0],[1,0],[0,1],[1,1]]):
	# 		for state in [[0,0,0],[0,0,1],[1,0,0],[1,0,1],[0,1,0],[0,1,1],[1,1,0],[1,1,1]]:
	# 			cost = 0
	# 			state_np = np.asarray(state)
	# 			for i in range(self.out_size):
	# 				cost+= (state_np.dot(self.G[0,i,:])+encoding[i])%2
	# 			self.pre_compute_cost[key].append(cost)
	def get_pre_commpute_table(self):
		self.pre_compute_table.append(np.asarray([[0, 0, 0], [0, 0, 1]]))
		self.pre_compute_table.append(np.asarray([[1, 0, 0], [1, 0, 1]]))
		self.pre_compute_table.append(np.asarray([[0, 1, 0], [0, 1, 1]]))
		self.pre_compute_table.append(np.asarray([[1, 1, 0], [1, 1, 1]]))


	def path_cost(self,index):
		return self.trellis[self.trellis_dict[index],self.current_location-1,1]
	def branch_cost(self,index,encoded_bits):
		if self.is_hard_encoder:
			predicted_bits1 = np.sum(self.pre_compute_table[index][0, :] * self.G[0, :, :], axis=1)
			predicted_bits2 = np.sum(self.pre_compute_table[index][1, :] * self.G[0, :, :],axis=1)
			encoded_bits = (encoded_bits>0).astype(int)
			return np.asarray([np.sum((predicted_bits1+encoded_bits)%2),np.sum((predicted_bits2+encoded_bits)%2)])
		else:
			predicted_bits1 = np.sum(self.pre_compute_table[index][0, :] * self.G[0, :, :], axis=1)%2
			predicted_bits2 = np.sum(self.pre_compute_table[index][1, :] * self.G[0, :, :], axis=1)%2
			predicted_bits1 = -(-1)**predicted_bits1
			predicted_bits2 = -(-1) ** predicted_bits2
			return np.asarray(
				[np.linalg.norm(predicted_bits1-encoded_bits),np.linalg.norm(predicted_bits2-encoded_bits)])


	def decode(self,encoded_bits):

		for i in range(self.NUM_STATES):
			temp_array = self.path_cost(i)+self.branch_cost(i,encoded_bits)
			index = np.argmin(temp_array)
			self.trellis[i,self.current_location,0] = self.trellis_dict[i][index]
			self.trellis[i, self.current_location, 1] = temp_array[index]

		decoding_index = np.argmin(self.trellis[:,self.current_location,1])
		for i in range(self.decision_lag):
			decoding_index = int(self.trellis[decoding_index,self.current_location-i,0])
		decoding = decoding_index%2

		self.current_location+=1
		self.current_location%=self.decision_lag



		return decoding


