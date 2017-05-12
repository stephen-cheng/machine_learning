import sys
import node_sim_stage_linear as nssl

def except_judge(stage_id,threshold):
	dataset=nssl.node_sim(stage_id)
	if dataset == []:
		return [],[],[]
	else:
		nodes=dataset.keys()
		meanlist=list()
		nodelist=[]
		nodevalue=[]
		outlier_list=['The abnormal nodes at this stage: ']
		for data in dataset.values():
			total=sum(data.values())
			mean=total/len(data.values())
			meanlist.append(mean)
		for each in meanlist:
			if each < threshold:
				outlier = nodes[meanlist.index(each)]
				outlier_list.append(outlier)
			nodelist.append(nodes[meanlist.index(each)])
			nodevalue.append(each)
		if len(outlier_list) <= 1:
			outlier_list = ['No abnormal nodes at this stage !']
		return outlier_list, nodelist, nodevalue
		
if __name__ == '__main__':
	stage_id=sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	#threshold=sys.argv[2]
	threshold=0.5
	outlier,node_list,node_value_mean=except_judge(stage_id,threshold)
	if node_list == []:
		print "Insufficient Data !"
	else:
		print outlier
		print "Similarity (%s, other nodes): %s" %(node_list,node_value_mean)
		pass
