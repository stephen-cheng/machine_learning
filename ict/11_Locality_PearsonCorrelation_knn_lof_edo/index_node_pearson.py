import sys
import index_pearson as ip
	
def node_index_pair(index_list, node_list):
	node_dict = {}
	nodes = set(node_list)
	node_index = zip(node_list, index_list)
	for n in nodes:
		node_dict[n] = []
	for ni in node_index:
		node_dict.get(ni[0]).append(ni[1])
	return node_dict
	
def node_con(node_dict1, node_dict2):
	nodes = [node for node in node_dict1.keys() if node in node_dict2.keys()]
	return nodes
		
if __name__=='__main__':
	stage_id = sys.argv[1]
	index1 = sys.argv[2]
	index2 = sys.argv[3]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	myStage = ip.IndexPearson(stage_id)
	dataX, dataY, nodeX, nodeY = myStage.node_index(index1, index2)
	myPearson = myStage.pearson(dataX, dataY)
	print 'Pearson of [%s] and [%s]: ' % (index1, index2), myPearson
	node_dictX = node_index_pair(dataX, nodeX)
	node_dictY = node_index_pair(dataY, nodeY)
	nodes = node_con(node_dictX, node_dictY)
	for n in nodes:
		if len(node_dictX[n]) != len(node_dictY[n]):
			minLen = min(len(node_dictX[n]), len(node_dictY[n]))
			node_dictX[n] = node_dictX[n][:minLen]
			node_dictY[n] = node_dictY[n][:minLen]
		nodePearson = myStage.pearson(node_dictX[n], node_dictY[n])
		print 'Pearson of [%s] and [%s] on node %s: ' % (index1, index2, n), nodePearson
	
