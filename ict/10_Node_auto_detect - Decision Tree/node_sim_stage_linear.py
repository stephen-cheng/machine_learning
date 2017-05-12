import InsertTools
import sys
import time
import numpy as np

def node_sim(stage_id):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	# get app_id
	sql="select app_id, submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	if res == ():
		sim = []
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
		sql="select node, avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band),avg(netS_band),avg(netR_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" %(startTime,endTime)
		cur.execute(sql)
		res=cur.fetchall()
		nodes={}
		for r in res:
			if r[0] in slaves_node:
				nodes[r[0]]=list(r[1:])
		sql="select node,avg(ipc),avg(L2_MPKI),avg(L3_MPKI),avg(DTLB_MPKI),avg(ITLB_MPKI),avg(L1I_MPKI),avg(MUL_Ratio),avg(DIV_Ratio),avg(FP_Ratio),avg(LOAD_Ratio),avg(STORE_Ratio),avg(BR_Ratio) from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" %(startTime,endTime)
		cur.execute(sql)
		res=cur.fetchall()
		for r in res:
			n=nodes.get(r[0],None)
			if n is None:continue;
			n.extend(list(r[1:]))
			sim={}.fromkeys(nodes.keys())
		for k in sim:
			sim[k]={}.fromkeys(nodes.keys())
		for i in nodes:
			for j in nodes:
				sim[i][j]=sim_cos(normalarray(nodes[i],weights(stage_id)),normalarray(nodes[j],weights(stage_id)))		
	cur.close()
	conn.commit()
	conn.close
	return sim
	
def sim_cos(a,b):
	if a is None or b is None:
		pass
	else:
		return np.sum(a*b)/(np.sqrt(np.sum(a*a))*np.sqrt(np.sum(b*b)))
	
def normalarray(a,weights):
	if weights is None:
		w=np.ones(len(a))
	else:w=np.array(weights)
	res=[]
	for i in a:
		res.append(float(i))
	if np.array(res).shape != w.shape:
		pass
	else:
		return np.array(res)*(1.0/w)
	
def weights(stage_id):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	startTime=int(res[0][0])
	endTime=int(res[0][1])
	
	#get max from os
	sql1="select max(cpu_usage),max(mem_usage),max(ioWaitRatio),max(weighted_io),max(diskR_band),max(diskW_band),max(netS_band),max(netR_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000;" %(startTime,endTime)
	cur.execute(sql1)
	res1=cur.fetchall()
	r1=list(res1)
	for each in r1:
		e1 = each
		
	#get max from log
	sql2="select max(ipc),max(L2_MPKI),max(L3_MPKI),max(DTLB_MPKI),max(ITLB_MPKI),max(L1I_MPKI),max(MUL_Ratio),max(DIV_Ratio),max(FP_Ratio),max(LOAD_Ratio),max(STORE_Ratio),max(BR_Ratio) from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000;" %(startTime,endTime) 
	cur.execute(sql2)
	res2=cur.fetchall()
	r2=list(res2)
	for each in r2:
		e2 = each
	e=e1+e2
	cur.close()
	conn.commit()
	conn.close()
	return list(e)
	
if __name__ == '__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	sims = node_sim(stage_id)
	if sims == []:
		print "Insufficient Data !"
	else:
		print sims
		pass

