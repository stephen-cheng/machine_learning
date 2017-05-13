from math import sqrt
import InsertTools
import sys
import time
import numpy as np

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
	local_num=[1.0,2.0,3.0,4.0,5.0]
	node_x,node_y,node_l,node_locality,node_locality_mean,node_locality_all=[],[],[],[],[],[]
	for data in datas.values():
		x,y,l,locality_index,node_local_duration,local_duration_mean=[],[],[],[],[],[]
		for d in data:
			if d[0] in locality:
				x=x+[local_num[locality.index(d[0])]]
				y=y+[float(d[1])]
				l=l+[locality[locality.index(d[0])]]
				x[0]=x[0]+0.5
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
			local_duration_mean.append(np.mean(local_duration))
		node_x.append(x)
		node_y.append(y)
		node_l.append(l)
		node_locality.append(locality_type)
		node_locality_mean.append(local_duration_mean)
		node_locality_all.append(node_local_duration)
	#get duration mean
	duration_sum=[]
	for ny in node_y:
		duration_sum+=ny
	duration_mean=np.mean(duration_sum)
	#proportion of duration over mean group by locality
	node_locality_ratio=[]
	for nla in node_locality_all:
		locality_ratio_list=[]
		for n in nla:
			locality_no=len([x for x in n if x > duration_mean])
			locality_ratio=locality_no*1.0/len(n)
			locality_ratio_list.append(locality_ratio)
		node_locality_ratio.append(locality_ratio_list)
	cur.close()
	conn.commit()
	conn.close
	return nodes,node_x,node_y,node_locality,node_locality_mean,duration_mean,node_locality_ratio

def multiply(a,b):
	sum_ab=0.0
	for i in range(len(a)):
		temp=a[i]*b[i]
		sum_ab+=temp
	return sum_ab

def cal_pearson(x,y):
	n=len(x)
	sum_x=sum(x)
	sum_y=sum(y)
	sum_xy=multiply(x,y)
	sum_x2 = sum([pow(i,2) for i in x])
	sum_y2 = sum([pow(j,2) for j in y])
	molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
	denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
	return molecular/denominator

if __name__=='__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	nodes,data_x,data_y,data_locality,node_locality_mean,duration_mean,node_locality_ratio=node_data(stage_id)
	data_pearson,data_dif=[],[]
	for n in nodes:
		x=data_x[nodes.index(n)]
		y=data_y[nodes.index(n)]
		if len(x) > 1:
			data_pearson.append(cal_pearson(x,y))
			print "Node : Locality : Duration : Over-Mean-Duration-Ratio : Pearson Correlation --> %s : %s : %s : %s:" % (n,data_locality[nodes.index(n)],node_locality_mean[nodes.index(n)],node_locality_ratio[nodes.index(n)]),cal_pearson(x,y)
		else:
			data_dif.append(n)
	#print "Pearson Correlation of Locality %s and Duration %s on %s: " % (data_locality,duration_mean,list(set(nodes).difference(set(data_dif)))), data_pearson
	print "Duration Mean of stage: ", duration_mean
	if data_dif != []:
		print "%s data is less than 2 !" % data_dif
