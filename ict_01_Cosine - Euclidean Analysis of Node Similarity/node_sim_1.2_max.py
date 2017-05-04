import InsertTools
import sys
import time
import json 
import numpy as np

def getSim(app_id):
    conn=InsertTools.getConnection()
    cur=conn.cursor()
    #sql1="select a.stage_id,a.task_host,a.deviation,b.cpu_usage,b.mem_usage from (select x.stage_id,x.task_host,abs(x.taskcount-y.avgcount)/y.avgcount as deviation from (select stage_id,task_host,count(task_id) as taskcount from task where app_id='%s' group by stage_id,task_host)x inner join (select t.stage_id as stage_id,avg(t.taskcount) as avgcount from (select stage_id,task_host,count(task_id) as taskcount from task where app_id='%s' group by stage_id,task_host)t group by t.stage_id)y on x.stage_id=y.stage_id)a inner join (select stage_id,node,avg(cpu_usage) as cpu_usage , avg(mem_usage) as mem_usage from os , (select stage_id , submission_time , completion_time from stage where app_id='%s')t where timestamp_>=submission_time/1000 and timestamp_<completion_time/1000 group by stage_id,node)b on a.stage_id=b.stage_id and a.task_host=b.node;" %(app_id,app_id,app_id)
    #sql2="select a.task_host,avg(a.deviation),avg(b.cpu_usage),avg(b.mem_usage),avg(b.ioWaitRatio),avg(b.weighted_io),avg(b.diskR_band),avg(b.diskW_band),avg(b.netS_band),avg(b.netR_band) from (select x.stage_id,x.task_host,abs(x.taskcount-y.avgcount)/y.avgcount as deviation from (select stage_id,task_host,count(task_id) as taskcount from task where app_id='%s' group by stage_id,task_host)x inner join (select t.stage_id as stage_id,avg(t.taskcount) as avgcount from (select stage_id,task_host,count(task_id) as taskcount from task where app_id='%s' group by stage_id,task_host)t group by t.stage_id)y on x.stage_id=y.stage_id)a inner join (select stage_id,node,avg(cpu_usage) as cpu_usage , avg(mem_usage) as mem_usage,avg(ioWaitRatio) as ioWaitRatio ,avg(weighted_io) as weighted_io,avg(diskR_band) as diskR_band,avg(diskW_band) as diskW_band,avg(netS_band) as netS_band, avg(netR_band) as netR_band from os , (select stage_id , submission_time , completion_time from stage where app_id='%s')t where timestamp_>=submission_time/1000 and timestamp_<completion_time/1000 group by stage_id,node)b on a.stage_id=b.stage_id and a.task_host=b.node group by a.task_host;" %(app_id,app_id,app_id)
    sql2="select node,avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band),avg(netS_band),avg(netR_band) from os,(select stage_id , submission_time , completion_time from stage where app_id='%s')t where timestamp_ >=t.submission_time/1000 and timestamp_ <= t.completion_time/1000 group by node;" %(app_id)
    cur.execute(sql2)
    rows=cur.fetchall()
    stages=set([r[0] for r in rows])
    values={}
    for n in stages:
	values[n]={}
    for r in rows:
        values[r[0]][r[1]]=r[2:]
    sim={}
    for i in range(len(rows)):
	j=i+1
	while j<len(rows):
		sim[(rows[i][0],rows[j][0])]=sim_cos(normalarray(rows[i][1:]),normalarray(rows[j][1:]))
		#print(rows[i][0]+","+rows[j][0]+":"+str(sim_cos(normalarray(rows[i][1:]),normalarray(rows[j][1:]))))
		j+=1
    print(sim)
    cur.close()
    conn.commit()
    conn.close()
    return sim
	
def getSim_stage(app_id,stage_id):
    conn=InsertTools.getConnection()
    cur=conn.cursor()
    sql="select node,avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band),avg(netS_band),avg(netR_band) from os,(select stage_id , submission_time , completion_time from stage where app_id='%s' and stage_id='%s')t where timestamp_ >=t.submission_time/1000 and timestamp_ <= t.completion_time/1000 group by node;" %(app_id,stage_id)
    cur.execute(sql)
    rows=cur.fetchall()
    stages=set([r[0] for r in rows])
    values={}
    for n in stages:
	values[n]={}
    for r in rows:
        values[r[0]][r[1]]=r[2:]
    sim={}
    for i in range(len(rows)):
	j=i+1
	while j<len(rows):
		sim[(rows[i][0],rows[j][0])]=sim_cos(normalarray(rows[i][1:]),normalarray(rows[j][1:]))
		#print(rows[i][0]+","+rows[j][0]+":"+str(sim_cos(normalarray(rows[i][1:]),normalarray(rows[j][1:]))))
		j+=1
    #normalization
    arr=np.array(sim.values())
    std=np.std(arr)
    mean=np.mean(arr)
    for k in sim:
        sim[k]=(sim[k]-mean)/std
    #normalization end
    cur.close()
    conn.commit()
    conn.close()
    return sim
	
def newSim(app_id,stage_id,weights=None):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	startTime=int(res[0][0])
	endTime=int(res[0][1])
	
	sql="select node,avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band),avg(netS_band),avg(netR_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" %(startTime,endTime)
	cur.execute(sql)
	res=cur.fetchall()
	nodes={}
	for r in res:
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
			sim[i][j]=sim_cos(normalarray(nodes[i],weights),normalarray(nodes[j],weights))
	print sim
	cur.close()
	conn.commit()
	conn.close()
	return sim
	
def sim_cos(a,b):
    return np.sum(a*b)/(np.sqrt(np.sum(a*a))*np.sqrt(np.sum(b*b)))
	
def normalarray(a,weights=None):
	if weights is None:
		w=np.ones(len(a))
	else:w=np.array(weights)
	res=[]
	for i in a:
		res.append(float(i))
	return np.array(res)/w
	
if __name__ == '__main__':
    #app_id=sys.argv[1]
    #stage_id=sys.argv[2]
    app_id="app-20160719212517-0001"
    stage_id="spark_stage_app-20160719212517-0001_2"
    #getSim_stage(app_id,stage_id)

    #weights is an object, so changing the weights should be done in this file.
    weights=[1,0.8,1,500000,300000000,300000000,200000000,200000000,3,250,120,25,15,450,0.25,0.03,0.07,2.5,1,1]
    newSim(app_id,stage_id,weights)
    pass
