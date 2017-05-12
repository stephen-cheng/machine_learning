#-*- coding: utf-8 -*-
import InsertTools
import sys
import time
import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import svm
	
def node_dect(stage_id,node_i):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time ,completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	if res == ():
		value_normal = []
	else:
		startTime=int(res[0][0])
		endTime=int(res[0][1])
		sql="select node,cpu_usage,mem_usage,ioWaitRatio,weighted_io,diskR_band,diskW_band,netS_band,netR_band from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i)
		cur.execute(sql)
		res=cur.fetchall()
		nodes={}
		os_normal_list = []
		for r in res:
			nodes[r[0]] = list(r[1:])
			for v in nodes.values():
				os_value_list = normal_array(v,weights_os(stage_id,node_i))
				for each in os_value_list:
					os_normal_list.append(each)
		sql="select node,ipc,L2_MPKI,L3_MPKI,DTLB_MPKI,ITLB_MPKI,L1I_MPKI,MUL_Ratio,DIV_Ratio,FP_Ratio,LOAD_Ratio,STORE_Ratio,BR_Ratio from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i)
		cur.execute(sql)
		res2=cur.fetchall()
		nodes2={}
		log_normal_list = []
		for r in res2:
			nodes2[r[0]] = list(r[1:])
			for v in nodes2.values():
				log_value_list = normal_array(v,weights_log(stage_id,node_i))
				for each in log_value_list:
					log_normal_list.append(each)
		value_normal=os_normal_list+log_normal_list
		value_normal2=value_normal
		random.shuffle(value_normal)
		array1=np.array(value_normal)
		random.shuffle(value_normal2)
		array2=np.array(value_normal2)
		normal_list=np.vstack((array1,array2))
		datalist=np.transpose(normal_list)
		
		#draw one_clss_SVM
		oneClassSVM(datalist,node_i)
	cur.close()
	conn.commit()
	conn.close()
	return value_normal
	
def normal_array(x,weights):
	if weights is None:
		w=np.ones(len(x))
	else:w=np.array(weights)
	vals=[]
	for i in x:
		vals.append(float(i))
	if np.array(vals).shape != w.shape:
		pass
	else:
		return np.array(vals)/w
	
def weights_os(stage_id,node_i):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time ,completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	startTime=int(res[0][0])
	endTime=int(res[0][1])
	
	#get max from os
	sql1="select max(cpu_usage),max(mem_usage),max(ioWaitRatio),max(weighted_io),max(diskR_band),max(diskW_band),max(netS_band),max(netR_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i)
	cur.execute(sql1)
	res1=cur.fetchall()
	r1=list(res1)
	for each in r1:
		e1 = each
	weight_list=list(e1)
	cur.close()
	conn.commit()
	conn.close()
	return weight_list
	
def weights_log(stage_id,node_i):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time ,completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	startTime=int(res[0][0])
	endTime=int(res[0][1])
	
	#get max from log
	sql2="select max(ipc),max(L2_MPKI),max(L3_MPKI),max(DTLB_MPKI),max(ITLB_MPKI),max(L1I_MPKI),max(MUL_Ratio),max(DIV_Ratio),max(FP_Ratio),max(LOAD_Ratio),max(STORE_Ratio),max(BR_Ratio) from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(startTime, endTime, node_i)
	cur.execute(sql2)
	res2=cur.fetchall()
	r2=list(res2)
	for each in r2:
		e2 = each
	weight_list=list(e2)
	cur.close()
	conn.commit()
	conn.close()
	return weight_list
	
def oneClassSVM(dataset,node_i):
	xx, yy = np.meshgrid(np.linspace(-1, 2, 500), np.linspace(-1, 2, 500))
	# Generate train data
	threshold = len(dataset) * 1/3 # set train nums
	X_train = dataset[:threshold,]
	# Generate some regular novel observations
	X_test = dataset[threshold:,]
	
	# Generate some abnormal novel observations
	#X_outliers = np.random.uniform(low=-0.1, high=0.1, size=(50, 2))

	# fit the model
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(X_train)
	y_pred_train = clf.predict(X_train)
	y_pred_test = clf.predict(X_test)
	#y_pred_outliers = clf.predict(X_outliers)
	n_error_train = y_pred_train[y_pred_train == -1].size
	n_error_test = y_pred_test[y_pred_test == -1].size
	#n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

	# plot the line, the points, and the nearest vectors to the plane
	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)

	plt.title("Anomaly Detection")
	plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 8), cmap=plt.cm.Blues_r)
	a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='red')
	plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='orange')

	b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white')
	b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='green')
	#c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='red')
	plt.axis('tight')
	plt.xlim((-1, 2))
	plt.ylim((-1, 2))
	#plt.legend([a.collections[0], b1, b2, c],["learned frontier", "training observations","new regular observations", "new abnormal observations"],loc="upper left", prop=matplotlib.font_manager.FontProperties(size=11))
	plt.legend([a.collections[0], b1, b2],
			   ["learned frontier", "training observations",
				"test observations"],
			   loc="upper left",
			   prop=matplotlib.font_manager.FontProperties(size=11))
	#plt.xlabel("error train: %d/%d ; errors novel regular: %d/%d ;" "errors novel abnormal: %d/20" % (n_error_train, X_train.size, n_error_test, X_test.size, n_error_outliers))
	plt.xlabel(
		"train errors: %d/%d ; test errors: %d/%d ; "
		% (n_error_train, X_train.size, n_error_test, X_test.size))
	plt.savefig('plot/single_node_one_class_svm_%s.png' % (node_i))
	#plt.show()
	
if __name__ == '__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	node_list = ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"]
	node_i = node_list[0]
	node_dect(stage_id, node_i)
	if node_dect(stage_id, node_i) == []:
		print "Insufficient Data !"
	else:
		pass
