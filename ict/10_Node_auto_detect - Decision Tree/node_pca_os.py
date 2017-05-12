import InsertTools
import sys
import time
import json 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
	
def nodeIndex(stage_id, node_i):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql = "select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	normal_list = []
	if res == ():
		pass
	else:
		startTime = int(res[0][0])
		endTime = int(res[0][1])
		sql = "select node, cpu_usage, mem_usage, ioWaitRatio, weighted_io, diskR_band, diskW_band, netS_band, netR_band from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i)
		cur.execute(sql)
		res = cur.fetchall()
		nodes = {}
		for r in res:
			nodes[r[0]] = list(r[1:])
			for v in nodes.values():
				index_list = normalarray(v,weights(stage_id, node_i))
				normal_list.append(index_list)
	cur.close()
	conn.commit()
	conn.close()
	return normal_list
	
def normalarray(a,weights):
	if weights is None:
		w = np.ones(len(a))
	else:w = np.array(weights)
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res) * (1.0 / w)
	
def weights(stage_id, node_i):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql = "select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	startTime = int(res[0][0])
	endTime = int(res[0][1])
	
	sql1 = "select max(cpu_usage), max(mem_usage), max(ioWaitRatio), max(weighted_io), max(diskR_band), max(diskW_band), max(netS_band), max(netR_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i) 
	cur.execute(sql1)
	res1 = cur.fetchall()
	r1 = list(res1)
	for each in r1:
		e1 = each		
	return list(e1)
	
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
	eigval_sum = 0
	for each in eigVals_top:
		eigval_sum += each
		eigval_k = eigval_sum / sum(eigVals_top)
		if eigval_k >= 0.99:
			k = eigVals_top.index(each)+1
			break			
	eig_list = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
	# sort, sort goes smallest to largest
	eigValInd = np.argsort(eigVals)
	# cut off unwanted dimensions
	eigValInd = eigValInd[:-(topNfeat+1):-1]
	eig_recommed = []
	for each in eigValInd[:k]:
		str = eig_list[each]
		eig_recommed.append(str)
	# reorganize eig vects largest to smallest
	redEigVects = eigVects[:,eigValInd]
	nRedDim = k
	if nRedDim>0:
		redEigVects = eigVects[:,:nRedDim]
	# transform data into new dimensions
	lowDDataMat = stded * redEigVects
	# The refactoring data matrix
	reconMat = (lowDDataMat * redEigVects.T) * np.std(dataMat) + meanVals
	return lowDDataMat, reconMat, eig_recommed
	
def plotBestFit(dataSet1,dataSet2,node_i):
	dataArr1 = np.array(dataSet1)
	dataArr2 = np.array(dataSet2)
	n = np.shape(dataArr1)[0] 
	#n1 = np.shape(dataArr2)[0]
	xcord1 = []; ycord1 = []
	xcord2 = []; ycord2 = []
	for i in range(n):
		xcord1.append(dataArr1[i,0].real); ycord1.append(dataArr1[i,1].real)
		xcord2.append(dataArr2[i,0].real); ycord2.append(dataArr2[i,1].real)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(xcord1, ycord1, s=30, c='red', marker='s', label="lowDataSet")
	ax.scatter(xcord2, ycord2, s=30, c='blue', label="rawDataSet")
	plt.xlabel('X'); plt.ylabel('Y');
	plt.legend(loc=2)
	plt.savefig('plot/single_node_pca_os_%s.png' % (node_i))
	#plt.show() 
	
if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	node_list = ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"]
	node_i = node_list[0]
	data = nodeIndex(stage_id, node_i)
	if data == []:
		print "Insufficient Data !"
	else:
		low, raw, pca_data = pca(data, 8, 8)
		print "Recommended features as PCA:", pca_data
		plotBestFit(low,raw,node_i)
	
