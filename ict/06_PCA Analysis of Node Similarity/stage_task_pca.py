import InsertTools
import sys
import time
import json 
import numpy as np
import matplotlib.pyplot as plt
	
def nodeIndex(stage_id,weights):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	#node_list = ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"]
	sql = "select task_host, cpu_usage, ioWaitRatio, weighted_io, mem_usage, diskR_band, diskW_band, netS_band, netR_band, ipc, L2_MPKI, L1I_MPKI, L3_MPKI from task where stage_id = '%s';" % (stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	nodes = {}
	normal_list = []
	for r in res:
		nodes[r[0]] = list(r[1:])
		for v in nodes.values():
			index_list = normalarray(v,weights)
			normal_list.append(index_list)
	normal_list = np.nan_to_num(normal_list)
	#print normal_list	
	cur.close()
	conn.commit()
	conn.close()
	return normal_list
	
def normalarray(a,weights=None):
	if weights is None:
		w = np.ones(len(a))
	else:w = np.array(weights)
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res) * (1.0 / w)
	
def weights():
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	node_list = ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"]
	sql= "select max(cpu_usage), max(ioWaitRatio), max(weighted_io), max(mem_usage), max(diskR_band), max(diskW_band), max(netS_band), max(netR_band), max(ipc), max(L2_MPKI), max(L1I_MPKI), max(L3_MPKI) from task where stage_id = '%s';" % (stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	r = list(res)
	for each in r:
		e = each		
	return list(e)
	
def pca(dataMat, nRedDim, topNfeat):
	meanVals = np.mean(dataMat, axis=0)
	# remove mean
	meanRemoved = dataMat - meanVals
	# The normalized standard deviation
	stded = meanRemoved / np.std(dataMat)
	covMat = np.cov(stded, rowvar=0)
	eigVals, eigVects = np.linalg.eig(np.mat(covMat))
	eigVals_sort = np.sort(eigVals)
	eigVals_top = list(eigVals_sort[::-1])
	print eigVals_top
	
	eigval_sum = 0
	for each in eigVals_top:
		eigval_sum += each
		eigval_k = eigval_sum / sum(eigVals_top)
		if eigval_k >= 0.99:
			break	
		k = eigVals_top.index(each)+1
	
	eig_list = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band', 'ipc', 'L2_MPKI', 'L1I_MPKI', 'L3_MPKI']
	# sort, smallest to largest
	eigValInd = np.argsort(eigVals)
	# cut off unwanted dimensions
	eigValInd = eigValInd[:-(topNfeat+1):-1]
	eig_recommed = []
	for each in eigValInd[:k]:
		str = eig_list[each]
		eig_recommed.append(str)
	print "Those features are recommended to retain as PCA:",eig_recommed
	# reorganize eig vects largest to smallest
	redEigVects = eigVects[:,eigValInd]
	nRedDim = k
	if nRedDim>0:
		redEigVects = eigVects[:,:nRedDim]
	# transform data into new dimensions
	lowDDataMat = stded * redEigVects
	# The refactoring data matrix
	reconMat = (lowDDataMat * redEigVects.T) * np.std(dataMat) + meanVals
	return lowDDataMat, reconMat
	
def plotBestFit(dataSet1,dataSet2):
	dataArr1 = np.array(dataSet1)
	dataArr2 = np.array(dataSet2)
	n = np.shape(dataArr1)[0] 
	#n1 = np.shape(dataArr2)[0]
	xcord1 = []; ycord1 = []
	xcord2 = []; ycord2 = []
	for i in range(n):
		xcord1.append(dataArr1[i,0]); ycord1.append(dataArr1[i,1])
		xcord2.append(dataArr2[i,0]); ycord2.append(dataArr2[i,1])
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(xcord1, ycord1, s=30, c='red', marker='s', label="lowDataSet")
	ax.scatter(xcord2, ycord2, s=30, c='blue', label="rawDataSet")
	plt.xlabel('X'); plt.ylabel('Y');
	plt.legend(loc=2)
	plt.show() 
	
if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	weights = weights()
	data = nodeIndex(stage_id,weights)
	low,raw = pca(data, 12, 12)
	plotBestFit(low,raw)
	pass
