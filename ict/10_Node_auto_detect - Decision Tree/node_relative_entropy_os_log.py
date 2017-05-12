import InsertTools
import sys
import time
import numpy as np
import node_outlier_judge as noj
#import node_pca as npa
	
def node_kl(stage_id,feature,table,node1,node2,bins):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
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
	threshold = 0.5
	outlier_sim, node, node_value_mean = noj.except_judge(stage_id,threshold)
	if node == []:
		print "Insufficient Data !"
	else:
	
		'''pca_list_p = []
		if len(outlier_sim) >= 2:
			for node_i in outlier_sim[1:]:
				data_pca = npa.nodeIndex(stage_id, node_i)
				low_pca, raw_pca, pca_pca = npa.pca(data_pca, 20, 20)
				npa.plotBestFit(low_pca,raw_pca,node_i)
				pca_list_p.extend(pca_pca)
			pca_list_pca = list(set(pca_list_p))
			pca_list_pca.sort(key=pca_list_p.index)
		else:
			data_pca = npa.nodeIndex(stage_id, node[0])
			low_pca, raw_pca, pca_pca = npa.pca(data_pca, 20, 20)
			npa.plotBestFit(low_pca,raw_pca,node[0])
			pca_list_p.extend(pca_pca)
			pca_list_pca = list(set(pca_list_p))
			pca_list_pca.sort(key=pca_list_p.index)
		print "Recommended features as PCA are: ", pca_list_pca'''
		pca_list_pca = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', \
		'netR_band', 'ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI']
		feature_list_os = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
		feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
		table_list = ['os', 'log']
		bins = 100
		
		for feature in pca_list_pca:
			re_value = []	
			re_value_avg_list = []
			if feature in feature_list_os:
				node_index_i = 0
				while (node_index_i<len(node)):
					node_j = node[node_index_i]
					for node_k in node:	
						table = table_list[0]
						re = node_kl(stage_id,feature,table,node_j,node_k,bins)
						re_value.append(re)
					node_index_i += 1		
				re_value_list = [re_value[i:i+len(node)] for i in xrange(0,len(re_value),len(node))]
				for rv in re_value_list:
					re_value_avg = sum(rv)/len(node)
					re_value_avg_list.append(re_value_avg)
				print '%s Relative Entropy mean value of %s between other nodes are: ' % (feature, node), re_value_avg_list								
			elif feature in feature_list_log:
				node_index_i = 0
				while (node_index_i<len(node)):
					node_j = node[node_index_i]
					for node_k in node:	
						table = table_list[1]
						re = node_kl(stage_id,feature,table,node_j,node_k,bins)
						re_value.append(re)			
					node_index_i += 1
				re_value_list = [re_value[i:i+len(node)] for i in xrange(0,len(re_value),len(node))]
				for rv in re_value_list:
					re_value_avg = sum(rv)/len(node)
					re_value_avg_list.append(re_value_avg)
				print '%s Relative Entropy mean value of %s between other nodes are: ' % (feature, node), re_value_avg_list	
			else:
				pass	
	
