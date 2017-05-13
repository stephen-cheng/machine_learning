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
	#euclidean metric outlier
	node_outlier_locality,node_outlier_duration,node_outlier_list=[],[],[]
	for n in nodes:
		nd=node_duration[nodes.index(n)]
		nl=node_locality[nodes.index(n)]
		outlier_locality,out_list=[],[]
		outlier_duration=outlier_detect(nd)
		for out_d in outlier_duration:
			outlier_locality.append(nl[nd.index(out_d)])
			outlier_index=nd.index(out_d)+1
			out=[outlier_index,out_d]
			out_list.append(out)
		node_outlier_duration.append(outlier_duration)
		node_outlier_locality.append(outlier_locality)
		node_outlier_list.append(out_list)
	cur.close()
	conn.commit()
	conn.close
	return nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,node_outlier_locality,node_outlier_duration,node_outlier_list
	
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
	#plt.legend((sa,sb),('Slow','Fast'),loc='upper left', numpoints=1, ncol=3, bbox_to_anchor=(0,-0.01))
	plt.savefig('plot/nodes_locality_knn_%s.png' % (node))
	plt.show()

if __name__=='__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0" #or 'spark_stage_application_1474358750931_0009_5'
	nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,node_outlier_locality,node_outlier_duration,node_outlier_list=node_data(stage_id)
	for node in nodes:
		#plot
		out_list=node_outlier_list[nodes.index(node)]
		duration_list=node_duration[nodes.index(node)]
		plotPic(duration_list,out_list,node)
		#count outlier
		locality_type=locality_list[nodes.index(node)]
		outlier_locality=node_outlier_locality[nodes.index(node)]
		outlier_duration=node_outlier_duration[nodes.index(node)]
		locaity_no=node_local_no[nodes.index(node)]
		locality_index,outlier_ratio,local_duration=[],[],[]
		for lt in locality_type:
			lt_index=[i for i,v in enumerate(outlier_locality) if v==lt]
			locality_index.append(lt_index)
			num_lt = outlier_locality.count(lt)		
			outlier_ra=float(num_lt)/locaity_no[locality_type.index(lt)]
			outlier_ratio.append(outlier_ra)
		for local_i in locality_index:
			out_duration=[]
			for li in local_i:
				out_duration.append(outlier_duration[li])
			local_duration.append(out_duration)	
		print "node : locality : outlier-ratio : duration-outlier --> %s : %s : %s : %s " % (node,locality_type,outlier_ratio,local_duration)
	print "Mean duration of stage: ",duration_mean
		
	
