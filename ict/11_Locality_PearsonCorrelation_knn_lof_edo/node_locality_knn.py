from math import sqrt
import InsertTools
import sys
import time
import operator
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def node_data(stage_id):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	# get locality and duration
	sql="select task_host, locality, duration from task where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	node=[]
	for r in res:
		node.append(r[0])
	nodes=list(set(node))
	datas={}
	for n in nodes:
		datas[n]=[]
	# grouping data by node	
	i=0
	for r in res:
		datas.values()[datas.keys().index(r[0])].append(r[1:])
	# tansform string into number
	locality=['PROCESS_LOCAL','NODE_LOCAL','NO_PREF','RACK_LOCAL','ANY']
	node_duration,node_locality,locality_list,node_locality_duration,node_local_no=[],[],[],[],[]
	for data in datas.values():
		y,l,locality_index,node_local_duration,locality_no=[],[],[],[],[]
		for d in data:
			if d[0] in locality:
				y=y+[float(d[1])]
				l=l+[locality[locality.index(d[0])]]
				locality_type=list(set(l))
		#classify duration by locality
		for li in locality_type:
			l_index=[i for i,v in enumerate(l) if v==li]
			locality_index.append(l_index)
		for lx in locality_index:
			local_duration=[]
			for lxi in lx:
				local_duration.append(y[lxi])
			node_local_duration.append(local_duration)
			locality_no.append(len(local_duration))
		node_duration.append(y)
		node_locality.append(l)
		locality_list.append(locality_type)
		node_locality_duration.append(node_local_duration)
		node_local_no.append(locality_no)
	#get duration mean
	duration_sum=[]
	for nd in node_duration:
		duration_sum+=nd
	duration_mean=np.mean(duration_sum)
	duration_no=len(duration_sum)
	# label values by knn
	node_locality_no,node_duration_mean_list,out_lists,outlier_locality_list,outlier_duration_list=[],[],[],[],[]
	for n in nodes:
		label_list,distance_list = [],[]
		nd=node_duration[nodes.index(n)]
		nl=node_locality[nodes.index(n)]
		node_duration_mean=np.mean(nd)
		node_duration_mean_list.append(node_duration_mean)
		node_locality_no.append(len(nd))
		a = float(max(nd))
		b = float(min(nd))
		for ndi in nd:
			label,distance = knn([ndi],a,b,1)
			label_list.append(label)
			distance_list.append(distance)	
		#detect outlier
		num_a = label_list.count('A')
		num_b = label_list.count('B')
		out_list,outlier_locality,outlier_duration=[],[],[]
		for i in range(len(label_list)):
			if label_list[i] == 'A' and nd[i] > duration_mean:
				out_locality = nl[i]
				out_duration = nd[i]
				out_index = i+1
				out = [out_index,out_duration]
				out_list.append(out)
				outlier_locality.append(out_locality)
				outlier_duration.append(out_duration)
		out_lists.append(out_list)
		outlier_locality_list.append(outlier_locality)
		outlier_duration_list.append(outlier_duration)
	cur.close()
	conn.commit()
	conn.close
	return nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,duration_no,node_duration_mean_list,node_locality_no,out_lists,outlier_locality_list,outlier_duration_list
	
def knn(inX, a, b, k):
	dataSet = [[a],[b]]
	dataSet = np.array(dataSet)
	labels = ['A','B']
	dataSetSize = dataSet.shape[0]
	diffMat = np.tile(inX, (dataSetSize,1)) - dataSet    
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
	
def plotPic(data,out_list,node):
	instances = []
	x = 1
	for each in data:
		instance = (x,each)
		x = x+1
		instances.append(instance)
	x,y = zip(*instances)
	sa=plt.scatter(x,y, s=20, color="#0000FF")
	for instance in out_list:
		sb=plt.scatter(instance[0], instance[1], color = "#FF0000")
	plt.title('%s knn plotting of locality-duration' % node)
	plt.legend((sa,sb),('Slow','Fast'),loc='upper left', numpoints=1, ncol=3, bbox_to_anchor=(0,-0.01))
	plt.savefig('plot/nodes_locality_knn_%s.png' % (node))
	plt.show()

if __name__=='__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0" #or 'spark_stage_application_1474358750931_0009_5'
	nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,duration_no,node_duration_mean_list,node_locality_no,out_lists,outlier_locality_list,outlier_duration_list=node_data(stage_id)
	for node in nodes:
		#plot
		out_list=out_lists[nodes.index(node)]
		duration_list=node_duration[nodes.index(node)]
		plotPic(duration_list,out_list,node)
		#count outlier
		locality_type=locality_list[nodes.index(node)]
		outlier_locality=outlier_locality_list[nodes.index(node)]
		locaity_no=node_local_no[nodes.index(node)]
		outlier_ratio=[]
		for lt in locality_type:
			num_lt = outlier_locality.count(lt)		
			outlier_ra=float(num_lt)/locaity_no[locality_type.index(lt)]
			outlier_ratio.append(outlier_ra)
		print "Node : Locality : locality-outlier-ratio --> %s : %s : %s " % (node,locality_type,outlier_ratio)
	print "nodes : locality-outlier --> %s : %s " % (nodes,outlier_locality_list)
	print "nodes : duration-outlier --> %s : %s " % (nodes,outlier_duration_list)
	print "Mean duration of stage: ",duration_mean
		
	
