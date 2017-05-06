#-*- coding: utf-8 -*-

import InsertTools
import sys
import time
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from sklearn import svm
	
def dataDetect(stage_name):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select node, cpu_usage, ioWaitRatio from stage_index where stage_name='%s';" %(stage_name)
	cur.execute(sql)
	res=cur.fetchall()
	#print res
	itemlist=list()
	eachlist=list()
	#normal
	for items in res:
		item=list(items[0:])
		itemlist.append(item)
	for eachitem in itemlist:
		eachitem = map(float, eachitem)
		it=np.array(eachitem)/np.array(maxi(stage_name))
		for each in it:
			eachlist.append(each)
	array1=np.array(eachlist)
	random.shuffle(eachlist)
	array2=np.array(eachlist)
	eachlist=np.vstack((array1,array2))
	#print eachlist.shape
	datalist=np.transpose(eachlist)
	#print datalist
	
	oneClassSVM(datalist)
	
	cur.close()
	conn.commit()
	conn.close()
	return itemlist
	
def maxi(stage_name):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql2="select max(node), max(cpu_usage), max(ioWaitRatio) from stage_index where stage_name='%s';" %(stage_name)
	cur.execute(sql2)
	res2=cur.fetchall()
	for items in res2:
		items = map(float, items)
		item=list(items)
	return item
	
def oneClassSVM(dataset):
	xx, yy = np.meshgrid(np.linspace(-0.5, 1.5, 500), np.linspace(-0.5, 1.5, 500))
	# Generate train data
	#X = 0.06 * np.random.randn(100, 2)
	threshold = 8 # set train nums
	X_train = dataset[:threshold,]
	# Generate some regular novel observations
	#X = 0.3 * np.random.randn(20, 2)
	#X_test = np.r_[X + 2, X - 2]
	X_test = dataset[threshold:,]
	#print X_test
	
	# Generate some abnormal novel observations
	X_outliers = np.random.uniform(low=-0.1, high=0.1, size=(20, 2))

	# fit the model
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(X_train)
	y_pred_train = clf.predict(X_train)
	y_pred_test = clf.predict(X_test)
	y_pred_outliers = clf.predict(X_outliers)
	n_error_train = y_pred_train[y_pred_train == -1].size
	n_error_test = y_pred_test[y_pred_test == -1].size
	n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

	# plot the line, the points, and the nearest vectors to the plane
	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)

	plt.title("Anomaly Detection")
	plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 8), cmap=plt.cm.Blues_r)
	a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='red')
	plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='orange')

	b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white')
	b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='green')
	c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='red')
	plt.axis('tight')
	plt.xlim((-0.5, 1.5))
	plt.ylim((-0.5, 1.5))
	plt.legend([a.collections[0], b1, b2, c],
			   ["learned frontier", "training observations",
				"new regular observations", "new abnormal observations"],
			   loc="upper left",
			   prop=matplotlib.font_manager.FontProperties(size=11))
	plt.xlabel(
		"error train: %d/%d ; errors novel regular: %d/%d ; "
		"errors novel abnormal: %d/20"
		% (n_error_train, X_train.size, n_error_test, X_test.size, n_error_outliers))
	plt.savefig('Anomaly Detection.png')
	plt.show()
	
if __name__ == '__main__':
	#stage_name=sys.argv[1]
	stage_name="map at WordCount.scala:28"
	dataDetect(stage_name)
	pass
