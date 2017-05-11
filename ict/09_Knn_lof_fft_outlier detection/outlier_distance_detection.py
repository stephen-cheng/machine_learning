import numpy as np

def outlier_detect(data):
	distance_list,distance_suspect,data_index,outlier = [],[],[],[]
	data_median = get_median(data)
	for d in data:
		distance_list.append(abs(d-data_median))
	distance_mean = np.mean(distance_list)
	for dl in distance_list:
		if dl > distance_mean:
			distance_suspect.append(dl)
			data_index.append(distance_list.index(dl))
	confidence_interval = np.std(data) * 1.96 #0.95
	for ds in distance_suspect:
		if abs(ds-distance_mean) > confidence_interval:
			outlier.append(data[data_index[distance_suspect.index(ds)]])
	return outlier

def get_median(data):
	data = sorted(data)
	size = len(data)
	if size % 2 ==0:
		median = (data[size//2]+data[size//2-1])/2
	if size % 2 ==1:
		median = data[(size-1)//2]
	return median

if __name__ == '__main__':
	pass
		
