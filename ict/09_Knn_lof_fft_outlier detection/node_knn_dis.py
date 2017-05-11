import InsertTools
import sys
from numpy import  *
import matplotlib
matplotlib.use('Agg')
import operator
from matplotlib import pyplot as pt

def taskPara(stage_id):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	para_list = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band', 'ipc', 'L2_MPKI', 'L1I_MPKI', 'L3_MPKI']
	sql = "select task_host, avg(%s) from task where stage_id = '%s' group by task_host;" % (para_list[0], stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	nodes = {}
	node_list = []
	value_list = []
	for r in res:
		node_list.append(r[0])
		value_list.append(r[1])
	# label values by knn
	a = float(max(value_list))
	b = float(min(value_list))
	label_list = []
	distance_list = []
	for d in value_list:
		label,distance = knn([d],a,b,1)
		label_list.append(label)
		distance_list.append(distance)
	#detect outlier
	num_a = label_list.count('A')
	num_b = label_list.count('B')
	i = 0
	out = []
	out_list = []
	if num_a <= num_b/2:
		for lab in label_list:
			for dis in distance_list:
				if lab == 'A' and dis[0] >= 0.3:
					out_node = node_list[i]
					out_value = value_list[i]
					out_index = i+1
					out = [out_index,out_value]
					out_list.append(out)
					print "Outlier: ",out_node,out_value
			i = i+1
	if num_b < num_a/2:
		for lab in label_list:
			for dis in distance_list:
				if lab == 'B' and dis[0] >= 0.3:
					out_node = node_list[i]
					out_value = value_list[i]
					out_index = i+1
					out = [out_index,out_value]
					out_list.append(out)
					print "Outlier: ",out_node,out_value
			i = i+1
	cur.close()
	conn.commit()
	conn.close()
	return value_list, para_list[0], label_list, out_list
	
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
	
def plotPic(data, out_list):
	instances = []
	x = 1
	for each in data:
		instance = (x,each)
		x = x+1
		instances.append(instance)
	x,y = zip(*instances)
	pt.scatter(x,y, s=20, color="#0000FF")
	for instance in out_list:
		pt.scatter(instance[0], instance[1], color = "#FF0000")
	pt.show()

if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	#stage_id = "spark_stage_app-20160714162322-0002_3"
	data, para, labels, outlier = taskPara(stage_id)
	print "The average %s of each node is: " % para, data,'\n'
	print "The labels of each node: ",labels
	plotPic(data, outlier)
		