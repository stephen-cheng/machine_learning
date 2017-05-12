import InsertTools
import sys
import time
import numpy as np
	
def node_kl(stage_id,feature,table,node1,node2,bins):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	if res == ():
		kl = []
	else:
		startTime=int(res[0][0])
		endTime=int(res[0][1])
		sql="select %s from %s where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(feature,table,startTime,endTime,node1)
		cur.execute(sql)
		rows1=cur.fetchall()
		node1_values=[r[0] for r in rows1]+list(np.linspace(0,1,bins))
		index_min = min(node1_values)
		index_max = max(node1_values)
		sql="select %s from %s where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(feature,table,startTime,endTime,node2)
		cur.execute(sql)
		rows2=cur.fetchall()
		node2_values=[r[0] for r in rows2]+list(np.linspace(0,1,bins))
		index_min = min(node2_values)
		index_max = max(node2_values)
		node_distribution=np.histogram(node1_values,bins=bins,range=[0,1])[0]
		node1_distribution=np.histogram(node1_values,bins=bins,range=[index_min,index_max])[0]+node_distribution
		node2_distribution=np.histogram(node2_values,bins=bins,range=[index_min,index_max])[0]+node_distribution
		node1_distribution=node1_distribution/float(np.sum(node1_distribution))
		node2_distribution=node2_distribution/float(np.sum(node2_distribution))	
		kl = KLDistance(node1_distribution,node2_distribution)
	cur.close()
	conn.commit()
	conn.close()
	return kl
	
def KLDistance(p,q):
	if p.any() > 0.000001:
		tp=np.asarray(p,dtype=np.float)
	if q.any() > 0.000001:
		tq=np.asarray(q,dtype=np.float)
	return np.sum(tp*np.log(tp/tq))
	
if __name__=='__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	feature_list_os = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	node_list = ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"]
	feature = feature_list_os[0]
	table = table_list[0]
	node_j = node_list[1]
	node_k = node_list[5]
	bins = 100
	
	if len(node_list) <= 2:
		print "Less than two nodes can not calculate relative entropy !"
	else:
		re = node_kl(stage_id,feature,table,node_j,node_k,bins)
		if re == []:
			print "Insufficient Data !"
		else:
			print '%s Relative Entropy of %s and %s is: ' % (feature, node_j, node_k), re
	if re > 0.2:
		print "%s relative entropy of abnormal node %s and %s: " % (feature,node_j,node_k),re
	else:
		print "Relative entropy can not find any abnormal node !"
	
