import node_sim_stage_linear
import sys
import json

def except_judge(stage_id,threshold):
	dataset=json.loads(node_sim_stage_linear.newSim(stage_id,weights))
	nodes=dataset.keys()
	meanlist=list()
	#print nodes
	for data in dataset.values():
		total=sum(data.values())
		mean=total/len(data.values())
		#print mean
		meanlist.append(mean)
	#print meanlist
	for each in meanlist:
		if each >= threshold:
			pass
		else:
			print "The node %s of stage %s is abnormal" %(nodes[meanlist.index(each)],stage_id)

if __name__ == '__main__':
	weights=node_sim_stage_linear.weights()
	#stage_id=sys.argv[1]
	stage_id="spark_stage_app-20160719212517-0001_2"
	#threshold=sys.argv[2]
	threshold=0.96
	
	except_judge(stage_id,threshold)
	pass