from numpy import *  
import time  
import matplotlib.pyplot as plt  
import InsertTools 
import sys
import node_sim_linear as nsl
  
# calculate Euclidean distance  
def euclDistance(vector1, vector2):  
    return sqrt(sum(power(vector2 - vector1, 2)))  
  
# init centroids with random samples  
def initCentroids(dataSet, k):  
    numSamples, dim = dataSet.shape  
    centroids = zeros((k, dim))  
    for i in range(k):  
        index = int(random.uniform(0, numSamples))  
        centroids[i, :] = dataSet[index, :]  
    return centroids  
  
# k-means cluster  
def kmeans(dataSet, k):  
    numSamples = dataSet.shape[0]  
    # first column stores which cluster this sample belongs to,  
    # second column stores the error between this sample and its centroid  
    clusterAssment = mat(zeros((numSamples, 2)))  
    clusterChanged = True  
  
    ## step 1: init centroids  
    centroids = initCentroids(dataSet, k)  
  
    while clusterChanged:  
        clusterChanged = False  
        ## for each sample  
        for i in xrange(numSamples):  
            minDist  = 100000.0  
            minIndex = 0  
            ## for each centroid  
            ## step 2: find the centroid who is closest  
            for j in range(k):  
                distance = euclDistance(centroids[j, :], dataSet[i, :])  
                if distance < minDist:  
                    minDist  = distance  
                    minIndex = j  
              
            ## step 3: update its cluster  
            if clusterAssment[i, 0] != minIndex:  
                clusterChanged = True  
                clusterAssment[i, :] = minIndex, minDist**2  
  
        ## step 4: update centroids  
        for j in range(k):  
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]  
            centroids[j, :] = mean(pointsInCluster, axis = 0)  
	#print clusterAssment
  
    #print 'Congratulations, cluster complete!'  
    return centroids, clusterAssment  
  
# show your cluster only available with 2-D data  
def showCluster(dataSet, k, centroids, clusterAssment):  
    numSamples, dim = dataSet.shape  
    if dim != 2:  
        print "Sorry! I can not draw because the dimension of your data is not 2!"  
        return 1  
  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    if k > len(mark):  
        print "Sorry! Your k is too large! please contact Zouxy"  
        return 1  
  
    # draw all samples  
    for i in xrange(numSamples):  
        markIndex = int(clusterAssment[i, 0])  
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    # draw the centroids  
    for i in range(k):  
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
  
    plt.show()  

if __name__ == '__main__':
	#load data  
	stage_id="spark_stage_app-20160719212517-0001_2"
	weights = nsl.weights()
	
	results = nsl.sim(stage_id,weights)
	nodes = results.keys()
	sim_values = results.values()
	node_values = []
	for each in sim_values:
		node_value = each.values()
		for i in node_value:
			node_values.append(i)
	dataSet = node_values
	dataSet = vstack((dataSet,dataSet))
	dataSet = transpose(dataSet)
	
	#clustering
	dataSet = mat(dataSet)  
	k = 2
	centroids, clusterAssment = kmeans(dataSet, k)  
  
	#show the result  
	showCluster(dataSet, k, centroids, clusterAssment)  
	