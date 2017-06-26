import numpy as np

def load_data(filename, n_features=None):
	f = open(filename, 'r')	
	line_list = []
	for line in open(filename):
		line = f.readline().strip().split('\t')
		if len(line) > 1:
			line= line[:n_features]
			line_list.append([float(i) for i in line])
		else:
			line_list.append([int(i) for i in line])
	line_array = np.array(line_list)
	f.close()
	return line_array

if __name__ == '__main__':
	filename = "data/train_set.txt"
	data = load_data(filename)
	print data