from math import sqrt
import InsertTools
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as pt
from node_lof_backup import outliers

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
	#list to tuple for lof
	node_outlier_locality,node_outlier_lof,node_outlier_duration=[],[],[]
	for n in nodes:
		nd=node_duration[nodes.index(n)]
		nl=node_locality[nodes.index(n)]
		instances_no=len(nd)
		instances,outlier_locality,outlier_lof,outlier_duration=[],[],[],[]
		for ndi in nd:
			instance=tuple([ndi,ndi])
			instances.append(instance)
		k=instances_no
		lof=outliers(k,instances)
		for outlier in lof:
			locality_out=nl[nd.index(outlier["instance"][0])]
			outlier_locality.append(locality_out)
			outlier_lof.append(outlier["lof"])
			outlier_duration.append(outlier["instance"][0])
		node_outlier_locality.append(outlier_locality)
		node_outlier_lof.append(outlier_lof)
		node_outlier_duration.append(outlier_duration)
		#plotFig(instances)
	cur.close()
	conn.commit()
	conn.close
	return nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,node_outlier_locality,node_outlier_lof,node_outlier_duration
	
def plotFig(instances):
	x,y = zip(*instances)
	pt.scatter(x,y, 20, color="#0000FF")
	for outlier in lof:
		value = outlier["lof"]
		instance = outlier["instance"]
		color = "#FF0000" if value > 1 else "#0000FF"
		pt.scatter(instance[0], instance[1], color=color, s=(value-1)**2*10+20)
	pt.show()

if __name__=='__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0" #or 'spark_stage_application_1474358750931_0009_5'
	nodes,node_locality,node_duration,locality_list,node_local_no,duration_mean,node_outlier_locality,node_outlier_lof,node_outlier_duration=node_data(stage_id)
	for n in nodes:
		locality_type=locality_list[nodes.index(n)]
		locaity_no=node_local_no[nodes.index(n)]
		outlier_locality=node_outlier_locality[nodes.index(n)]
		outlier_lof=node_outlier_lof[nodes.index(n)]
		outlier_duration=node_outlier_duration[nodes.index(n)]
		locality_index,local_duration,local_lof,outlier_ratio=[],[],[],[]
		for lt in locality_type:
			lt_index=[i for i,v in enumerate(outlier_locality) if v==lt]
			locality_index.append(lt_index)
			num_lt = outlier_locality.count(lt)		
			outlier_ra=float(num_lt)/locaity_no[locality_type.index(lt)]
			outlier_ratio.append(outlier_ra)
		for li in locality_index:
			out_duration,out_lof=[],[]
			for lii in li:
				out_duration.append(outlier_duration[lii])
				out_lof.append(outlier_lof[lii])
			local_duration.append(out_duration)	
			local_lof.append(out_lof)
		print "node : anomaly-locality : anomaly-duration : anomaly-lof : anomaly-locality-ratio --> %s : %s : %s : %s : %s" % (n,locality_type,local_duration,local_lof,outlier_ratio)
			
	
