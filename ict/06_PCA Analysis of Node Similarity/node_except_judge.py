import node_sim_stage_linear
#import node_sim_max_heatmap
import sys
import json

def except_judge(stage_id,threshold,weights):
	dataset=json.loads(node_sim_stage_linear.newSim(stage_id,weights))
	#dataset=json.loads(node_sim_max_heatmap.newSim(stage_id,weights))
	nodes=dataset.keys()
	meanlist=list()
	#print nodes
	for data in dataset.values():
		total=sum(data.values())
		mean=total/len(data.values())
		#print mean
		meanlist.append(mean)
		#print meanlist
		simi_threshold= float(threshold)
		#print simi_threshold
	for each in meanlist:
		if each >= simi_threshold:
			pass
		else:
			print "The node [%s] of stage [%s] is abnormal." %(nodes[meanlist.index(each)],stage_id)
		print "Similarity(%s, other nodes): %s" %(nodes[meanlist.index(each)],each)
		
if __name__ == '__main__':
	weights=node_sim_stage_linear.weights()
	#weights=node_sim_max_heatmap.weights()
	stage_id=sys.argv[1]
	threshold=sys.argv[2]
	#stage_id="spark_stage_app-20160719212517-0001_2"
	#threshold=0.96
	
	except_judge(stage_id,threshold,weights)
	pass
