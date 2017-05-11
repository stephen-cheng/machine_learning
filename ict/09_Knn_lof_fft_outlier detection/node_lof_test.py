import InsertTools
import sys
from numpy import  *
from matplotlib import pyplot as pt
from node_lof import outliers

def taskInstances(stage_id):
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
	i = 0
	instance = []
	instances = []
	for value_list[i] in value_list:
		value = value_list[i]
		instance = tuple([value,value])
		instances.append(instance)
		i = i + 1
	cur.close()
	conn.commit()
	conn.close()
	return instances, para_list[0], node_list, value_list

def plotFig(instances):
	x,y = zip(*instances)
	pt.scatter(x,y, 20, color="#0000FF")
	for outlier in lof:
		value = outlier["lof"]
		instance = outlier["instance"]
		color = "#FF0000" if value > 1 else "#0000FF"
		pt.scatter(instance[0], instance[1], color=color, s=(value-1)**2*10+20)
	pt.show()
	
if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	instances, para, node_list, data = taskInstances(stage_id)
	print "The average %s of each node is: " % para,data
	d_min = min(data)
	d_max = max(data)
	if abs(d_max-d_min)>0.2 and len(data)>2:	
		k=len(data)
		lof = outliers(k, instances)
		for outlier in lof:
			node = node_list[data.index(outlier["instance"][0])]
			print "Outlier: ",node, '\n',"Degree of outlier: ", outlier["lof"],'\n', "The average %s of outlier node: " % para, outlier["instance"][0]
		plotFig(instances)
	
	