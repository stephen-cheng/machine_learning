import InsertTools
import sys
from numpy import *
import numpy as np
import operator
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import node_fft as nf
import outlier_distance_detection as odd
import collections

def taskPara(value_list,dis):
	value_list_raw = value_list
	if max(value_list) > 1:
		value_list = normalarray2(value_list_raw)
		value_list = value_list.tolist()
	# calculating order of magnitude
	order_node,order_value = [],[]
	order_outlier_node,order_outlier_value,outlier_order_node = [],[],[]
	label_list = []
	out_list = []
	for each in value_list:
		if each > 0.0:
			order_value.append(int(np.log10(each)))
			order_node.append(node_list[value_list.index(each)])
	if min(order_value)-max(order_value) <= -2:
		order_outlier_node = order_node
		order_outlier_value = order_value
		outlier_order_value = odd.outlier_detect(order_outlier_value)
		for oov in outlier_order_value:
			outlier_value_count = outlier_order_value.count(oov)
			if outlier_value_count > 1:
				dd = collections.defaultdict(list)
				for k,va in [(v,i) for i,v in enumerate(outlier_order_value)]:
					dd[k].append(va)
				value_index = dd.values()[1:]
				for vi in value_index:
					for v in vi:
						outlier_order_node.append(order_outlier_node[v])
				break		
			else:		
				outlier_order_node.append(order_outlier_node[order_outlier_value.index(oov)])
				
	# label values by knn
	a = float(min(value_list))
	b = float(max(value_list))
	outlier_node=[]
	outlier_value=[]
	distance_list = []
	for vl in value_list:
		label,distance = knn([vl],a,b,1)
		label_list.append(label)
		distance_list.append(distance)
	# detect outlier
	num_a = label_list.count('A')
	num_b = label_list.count('B')
	i = 0
	out = []
	if num_a <= num_b:
		for dl in distance_list:
			if dl[1] >= dis and label_list[i] == 'A':	
				out_node = node_list[i]
				out_value = value_list[i]
				out_index = i+1
				out = [out_index,out_value]
				out_list.append(out)
				outlier_node.append(out_node)
				outlier_value.append(out_value)
			i = i+1
	else:
		for dl in distance_list:
			if dl[0] >= dis and label_list[i] == 'B':
				out_node = node_list[i]
				out_value = value_list[i]
				out_index = i+1
				out = [out_index,out_value]
				out_list.append(out)
				outlier_node.append(out_node)
				outlier_value.append(out_value)
			i = i+1
	outlier_node_old=outlier_node
	outlier_node=list(set(outlier_node))
	outlier_node.sort(key=outlier_node_old.index)
	outlier_value_old=outlier_value
	outlier_value=list(set(outlier_value))
	outlier_value.sort(key=outlier_value_old.index)
	return value_list_raw, value_list, label_list, out_list, outlier_node, outlier_value, order_outlier_node, order_outlier_value, outlier_order_node

	
def normalarray2(a):
	if a is None:
		w = np.ones(len(a))
	else:w = np.array(max(a))
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res)/w
	
def knn(inX, a, b, k):
	dataSet = [[a],[b]]
	dataSet = array(dataSet)
	labels = ['A','B']
	dataSetSize = dataSet.shape[0]
	diffMat = tile(inX, (dataSetSize,1)) - dataSet    
	sqDiffMat = diffMat**2
	sqDistances = sqDiffMat.sum(axis=1) 
	distances = sqDistances**0.5
	sortedDistances = distances.argsort()  
	classCount = {}
	for i in range(k):
		numOflabel = labels[sortedDistances[i]]
		classCount[numOflabel] = classCount.get(numOflabel,0) + 1 
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0],distances
	
def plotPic(data, out_list, feature):
	instances = []
	x = 1
	for each in data:
		instance = (x,each)
		x = x+1
		instances.append(instance)
	x,y = zip(*instances)
	plt.scatter(x,y, s=20, color="#0000FF")
	for instance in out_list:
		plt.scatter(instance[0], instance[1], color="#FF0000")
	plt.savefig('plot/nodes_single_feature_knn_%s.png' % (feature))
	#plt.show()

if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	feature_list_os = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	# distance setting
	dis=0.6
	node_list = nf.node(stage_id)
	for feature in feature_list_os:
		data_set = []
		table = table_list[0]
		for node in node_list:
			data_list = nf.node_data(stage_id,feature,table,node)
			if data_list != []:
				data_set.append(data_list)
		summit_list = nf.fft_plot(data_set,feature,node_list)
		value_list_raw, value_list, labels, outlier, outlier_node, outlier_value, order_outlier_node, order_outlier_value, outlier_order_node = taskPara(summit_list,dis)
		if outlier_order_node != []:
			print "Order Outliers: ", outlier_order_node
		else:
			print "KNN Outliers: ", outlier_node, outlier_value
		if order_outlier_node!= []:
			print "Disparity of order of magnitude (log10): ", order_outlier_node, order_outlier_value
		print "%s raw mean value of each node knn: " % feature, value_list_raw
		print "%s normalized mean value of each node knn: " % feature, value_list
		print "KNN Node labels: ",labels
		
	for feature in feature_list_log:
		data_set = []
		table = table_list[1]
		for node in node_list:
			data_list = nf.node_data(stage_id,feature,table,node)
			if data_list != []:
				data_set.append(data_list)
		summit_list = nf.fft_plot(data_set,feature,node_list)
		value_list_raw, value_list, labels, outlier, outlier_node, outlier_value, order_outlier_node, order_outlier_value, outlier_order_node = taskPara(summit_list,dis)
		if outlier_order_node != []:
			print "Order Outliers: ", outlier_order_node
		else:
			print "KNN Outliers: ", outlier_node, outlier_value
		if order_outlier_node!= []:
			print "Disparity of order of magnitude (log10): ", order_outlier_node, order_outlier_value
		print "%s raw mean value of each node knn: " % feature, value_list_raw
		print "%s normalized mean value of each node knn: " % feature, value_list
		print "KNN Node labels: ",labels
		
