import InsertTools
import sys
from numpy import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from node_lof import outliers

def taskInstances(stage_id,feature,table):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql="select app_id, submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	if res == ():
		value_list_raw, value_list, node_list, instances = [],[],[],[]
	else:
		app_id=res[0][0]
		startTime=int(res[0][1])
		endTime=int(res[0][2])
		# get slaves list
		sql="select slaves_list from app where app_id='%s';" %(app_id)
		cur.execute(sql)
		res=cur.fetchall()
		slaves_node=res[0][0]
		slaves_node.split(',')
		sql = "select node, avg(%s) from %s where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" % (feature,table,startTime,endTime)
		cur.execute(sql)
		res = cur.fetchall()
		nodes = {}
		node_list = []
		value_list = []
		for r in res:
			if r[0] in slaves_node:
				nodes[r[0]]=list(r[1:])
				node_list.append(r[0])
				value_list.append(r[1])
		value_list_raw = value_list
		#value_list = normalarray(value_list, weights(stage_id,feature,table))
		if max(value_list) > 1:
			value_list = normalarray2(value_list)
			value_list = value_list.tolist()
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
	return value_list_raw, value_list, node_list, instances
	
	
def normalarray2(a):
	if a is None:
		w = np.ones(len(a))
	else:w = np.array(max(a))
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res)/w
	
def normalarray(a,weights):
	if weights is None:
		w = np.ones(len(a))
	else:w = np.array(weights)
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res)/w
	
def weights(stage_id,feature,table):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql="select app_id, submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	app_id=res[0][0]
	startTime=int(res[0][1])
	endTime=int(res[0][2])
	# get slaves list
	sql="select slaves_list from app where app_id='%s';" %(app_id)
	cur.execute(sql)
	res=cur.fetchall()
	slaves_node=res[0][0]
	slaves_node.split(',')
	sql = "select node, max(%s) from %s where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" % (feature,table,startTime,endTime)
	cur.execute(sql)
	res = cur.fetchall()
	w_list = []
	for r in res:
		if r[0] in slaves_node:
			w_list.append(r[1])
	w_max = max(w_list)
	w_list = w_max*len(r[0])
	return w_list

def plotFig(instances,lof,feature):
	x,y = zip(*instances)
	plt.scatter(x,y, 20, color="#0000FF")
	for outlier in lof:
		value = outlier["lof"]
		instance = outlier["instance"]
		color = "#FF0000" if value > 1 else "#0000FF"
		plt.scatter(instance[0], instance[1], color=color, s=(value-1)**2*10+20)
	plt.savefig('plot/nodes_single_feature_lof_%s.png' % (feature))
	#plt.show()
	
def lof_detect(data,node_list,instances,lof_distance,lof_degree):
	d_min = min(data)
	d_max = max(data)
	outlier_list = []
	outlier_degree = []
	outlier_value = []
	k=len(data)
	lof = outliers(k, instances,lof_degree)
	if abs(d_max-d_min)>lof_distance and len(data)>2:
		for outlier in lof:
			node = node_list[data.index(outlier["instance"][0])]
			outlier_list.append(node)
			outlier_degree.append(outlier["lof"])
			outlier_value.append(outlier["instance"][0])
	else:
		outlier_list=[]
		outlier_degree=1
		outlier_value=None
	return lof,outlier_list,outlier_degree,outlier_value
	
if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	para_list = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band', 'ipc', 'L2_MPKI', 'L1I_MPKI', 'L3_MPKI'] 
	table_list = ['os', 'log']
	feature = para_list[0]
	table = table_list[0]
	value_list_raw, value_list, node_list, instances = taskInstances(stage_id,feature,table)
	if value_list_raw == []:
		print "Insufficient Data !"
	else:
		print "%s raw mean value of each node lof: " % feature, value_list_raw
		print "%s normalized mean value of each node lof: " % feature, value_list
		#node distance setting and lof_degree setting
		lof_distance = 0.2
		lof_degree = 1.02
		lof,outlier_node,outlier_degree,outlier_value = lof_detect(value_list,node_list,instances,lof_distance,lof_degree)
		print "LOF Outlier: ",outlier_node
		print "LOF Outlier degree: ", outlier_degree
		print "%s mean of outlier lof: " % feature, outlier_value
		plotFig(instances,lof,feature)
	
	