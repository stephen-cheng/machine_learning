#-*- coding: utf-8 -*-
import sys
import warnings
import xml.etree.ElementTree as et
import node_outlier_judge as noj
import node_sim_stage_linear as nssl
import node_kmeans as nk
import node_one_class_svm as nocs
import node_pca as npa
import node_knn as nn
import node_lof_test as nlt
import node_relative_entropy as nre


def node_sim_dect(stage_id,threshold):
	outlier_sim, node_list, node_value_mean = noj.except_judge(stage_id,threshold)
	node_value = nssl.node_sim(stage_id)
	return outlier_sim, node_list, node_value_mean, node_value

def sim_config():
	config=et.parse("node_sim_config.xml")
	root=config.getroot()
	sim_threshold=float(root.findtext("sim_threshold"))
	k_kmeans=int(root.findtext("k_kmeans"))
	dis_knn=float(root.findtext("dis_knn"))
	lof_distance=float(root.findtext("lof_distance"))
	lof_degree=float(root.findtext("lof_degree"))
	re_bins=int(root.findtext("re_bins"))
	re_threshold=float(root.findtext("re_threshold"))
	return sim_threshold,k_kmeans,dis_knn,lof_distance,lof_degree,re_bins,re_threshold
	
if __name__=='__main__':
	warnings.filterwarnings("ignore")
	## stage_id = "spark_stage_app-20160630230531-0000_0"
	stage_id = sys.argv[1]
	
	## print results into file
	file = open('file/%s_results.txt' % (stage_id),'a')
	file.write(stage_id+"\r\n")
	file.close
	
	## invoke node_sim_config xml file
	sim_threshold,k_kmeans,dis_knn,lof_distance,lof_degree,re_bins,re_threshold = sim_config()
	
	##————————similarity analysis of all nodes by mean vs. threshold————————##
	threshold = sim_threshold
	outlier_sim, node, node_value_mean, node_value = node_sim_dect(stage_id,threshold)
	print outlier_sim
	#print 'Similarity (%s, other nodes): %s' % (node, node_value_mean)
	#print 'similarity value of all nodes: ', node_value
	
	## print results into file
	file = open('file/%s_results.txt' % (stage_id),'a')
	file.write(" ".join(outlier_sim)+"\r\n")
	file.write('Similarity (%s, other nodes): %s' % (node, node_value_mean)+"\r\n")
	file.write('similarity value of all nodes: '+"\r\n")
	file.write(" ".join(node_value)+"\r\n")
	file.close()
	
	
	##————————similarity analysis of all nodes by kmeans————————##
	## clustering number setting and show the result
	k_kmeans = k_kmeans
	data_kmeans, centroids, clusterAssment = nk.load_data(node_value, k_kmeans)
	nk.showCluster(data_kmeans, k_kmeans, centroids, clusterAssment)
	
	
	##—————————similarity analysis of single node by one class svm, plotting will take quite a few minutes————————##
	## ["hw004", "hw089", "hw062", "hw073", "hw103", "hw114", "hw106"], node_i=node[0]
	#if len(outlier_sim) >= 2:
		#for node_i in outlier_sim[1:]:
			#nocs.node_dect(stage_id, node_i)
	#else:
		#nocs.node_dect(stage_id, node[0])
	
	
	##————————similarity analysis of single node by pca————————##
	#node_i=node[0]
	pca_list_p = []
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
	#print "Recommended features as PCA are: ", pca_list_pca
	
	## print results into file
	file = open('file/%s_results.txt' % (stage_id),'a')
	file.write("Recommended features as PCA are: "+"\r\n")
	file.write(" ".join(pca_list_pca)+"\r\n")
	file.close()
	
	
	##————————similarity analysis of all nodes on single feature by mean knn————————##
	feature_list_os = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band'] 
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	## node distance setting
	dis_knn = dis_knn
	feature_pca_os = [val for val in pca_list_pca if val in feature_list_os]
	feature_pca_log = [val for val in pca_list_pca if val in feature_list_log]
	for feature in feature_pca_os:
		table = table_list[0]
		value_list_raw, value_list, labels_knn, outlier_knn, outlier_node_knn, outlier_value_knn = nn.taskPara(stage_id,feature,table,dis_knn)
		#print "%s raw mean value of all nodes knn: " % feature, value_list_raw
		#print "%s normalized mean value of all nodes knn: " % feature, value_list
		#print "knn Nodes labels: ",labels_knn
		outlier_node_list_knn = []
		outlier_node_value_knn = []
		normal_node_list_knn = []
		normal_node_value_knn = []
		for node_i in outlier_node_knn:
			if node_i in outlier_sim[1:]:
				outlier_node_list_knn.append(node_i)
				outlier_node_value_knn.append(outlier_value_knn[outlier_node_knn.index(node_i)])
			else:
				normal_node_list_knn.append(node_i)
				normal_node_value_knn.append(outlier_value_knn[outlier_node_knn.index(node_i)])
		if outlier_node_list_knn != []:
			print "KNN found that abnormal feature values of abnormal nodes are: ", feature, outlier_node_list_knn, outlier_node_value_knn
		else:
			if normal_node_list_knn != []:
				print "However, KNN found a few anomaly feature values of normal nodes are: ", feature, normal_node_list_knn, normal_node_value_knn
		nn.plotPic(value_list,outlier_knn,feature)
		
		## print results into file
		file = open('file/%s_results.txt' % (stage_id),'a')
		file.write("%s raw mean value of all nodes knn: " % feature+"\r\n")
		file.write(str(value_list_raw)+"\r\n")
		file.write("%s normalized mean value of all nodes knn: " % feature+"\r\n")
		file.write(str(value_list)+"\r\n")
		file.write("knn Nodes labels: "+"\r\n")
		file.write(" ".join(labels_knn)+"\r\n")
		if outlier_node_list_knn != []:
			file.write("KNN found that abnormal feature values of abnormal nodes are: "+"\r\n")
			file.write(str(feature)+"\r\n")
			file.write(" ".join(outlier_node_list_knn)+"\r\n")
			file.write(str(outlier_node_value_knn)+"\r\n")
		else:
			if normal_node_list_knn != []:
				file.write("However, KNN found a few anomaly feature values of normal nodes are: "+"\r\n")
				file.write(str(feature)+"\r\n")
				file.write(" ".join(normal_node_list_knn)+"\r\n")
				file.write(str(normal_node_value_knn)+"\r\n")
		file.close()
		
	for feature in feature_pca_log:
		table = table_list[1]
		value_list_raw, value_list, labels_knn, outlier_knn, outlier_node_knn, outlier_value_knn = nn.taskPara(stage_id,feature,table,dis_knn)
		#print "%s raw mean value of all nodes knn: " % feature, value_list_raw
		#print "%s normalized mean value of all nodes knn: " % feature, value_list
		#print "knn Nodes labels: ",labels_knn
		outlier_node_list_knn = []
		outlier_node_value_knn = []
		normal_node_list_knn = []
		normal_node_value_knn = []
		for node_i in outlier_node_knn:
			if node_i in outlier_sim[1:]:
				outlier_node_list_knn.append(node_i)
				outlier_node_value_knn.append(outlier_value_knn[outlier_node_knn.index(node_i)])
			else:
				normal_node_list_knn.append(node_i)
				normal_node_value_knn.append(outlier_value_knn[outlier_node_knn.index(node_i)])
		if outlier_node_list_knn != []:
			print "KNN found that abnormal feature values of abnormal nodes are: ", feature, outlier_node_list_knn, outlier_node_value_knn
		else:
			if normal_node_list_knn != []:
				print "However, KNN found a few anomaly feature values of normal nodes are: ", feature, normal_node_list_knn, normal_node_value_knn
		nn.plotPic(value_list,outlier_knn,feature)
		
		## print results into file
		file = open('file/%s_results.txt' % (stage_id),'a')
		file.write("%s raw mean value of all nodes knn: " % feature+"\r\n")
		file.write(str(value_list_raw)+"\r\n")
		file.write("%s normalized mean value of all nodes knn: " % feature+"\r\n")
		file.write(str(value_list)+"\r\n")
		file.write("knn Nodes labels: "+"\r\n")
		file.write(" ".join(labels_knn)+"\r\n")
		if outlier_node_list_knn != []:
			file.write("KNN found that abnormal feature values of abnormal nodes are: "+"\r\n")
			file.write(str(feature)+"\r\n")
			file.write(" ".join(outlier_node_list_knn)+"\r\n")
			file.write(str(outlier_node_value_knn)+"\r\n")
		else:
			if normal_node_list_knn != []:
				file.write("However, KNN found a few anomaly feature values of normal nodes are: "+"\r\n")
				file.write(str(feature)+"\r\n")
				file.write(" ".join(normal_node_list_knn)+"\r\n")
				file.write(str(normal_node_value_knn)+"\r\n")
		file.close()
		
	
	##————————similarity analysis of all nodes on single feature by mean lof————————##
	## node distance setting and lof_degree setting
	lof_distance = lof_distance
	lof_degree = lof_degree
	feature_list_os = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band'] 
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	for feature in pca_list_pca:
		if feature in feature_list_os:
			table = table_list[0]
			value_list_raw, value_list, node_list_lof, instances_lof = nlt.taskInstances(stage_id,feature,table)
			#print "%s raw mean value of each node: " % feature, value_list_raw
			#print "%s normalized mean value of each node: " % feature, value_list
			lof,outlier_node_lof,outlier_degree_lof,outlier_value_lof = nlt.lof_detect(value_list,node_list_lof,instances_lof,lof_distance,lof_degree)
			outlier_node_list_lof = []
			outlier_node_value_lof = []
			normal_node_list_lof = []
			normal_node_value_lof = []
			for node_i in outlier_node_lof:
				if node_i in outlier_sim[1:]:
					outlier_node_list_lof.append(node_i)
					outlier_node_value_lof.append(outlier_value_lof[outlier_node_lof.index(node_i)])
				else:
					normal_node_list_lof.append(node_i)
					normal_node_value_lof.append(outlier_value_lof[outlier_node_lof.index(node_i)])
			if outlier_node_list_lof != []:
				print "LOF found that abnormal feature values of abnormal nodes are: ", feature, outlier_node_list_lof, outlier_node_value_lof
			else:
				if normal_node_list_lof != []:
					print "However, LOF found a few anomaly feature values of normal nodes are: ", feature, normal_node_list_lof, normal_node_value_lof
			#print "lof Outlier degree: ", outlier_degree_lof
			nlt.plotFig(instances_lof,lof,feature)
			
			## print results into file
			file = open('file/%s_results.txt' % (stage_id),'a')
			file.write("%s raw mean value of all nodes lof: " % feature+"\r\n")
			file.write(str(value_list_raw)+"\r\n")
			file.write("%s normalized mean value of all nodes lof: " % feature+"\r\n")
			file.write(str(value_list)+"\r\n")
			if outlier_node_list_knn != []:
				file.write("LOF found that abnormal feature values of abnormal nodes are: "+"\r\n")
				file.write(str(feature)+"\r\n")
				file.write(" ".join(outlier_node_list_lof)+"\r\n")
				file.write(str(outlier_node_value_lof)+"\r\n")
			else:
				if normal_node_list_lof != []:
					file.write("However, LOF found a few anomaly feature values of normal nodes are: "+"\r\n")
					file.write(str(feature)+"\r\n")
					file.write(" ".join(normal_node_list_lof)+"\r\n")
					file.write(str(normal_node_value_lof)+"\r\n")
			file.write("lof Outlier degree: "+"\r\n")
			file.write(str(outlier_degree_lof)+"\r\n")		
			file.close()
			
		elif feature in feature_list_log:
			table = table_list[1]
			value_list_raw, value_list, node_list_lof, instances_lof = nlt.taskInstances(stage_id,feature,table)
			#print "%s raw mean value of each node: " % feature, value_list_raw
			#print "%s normalized mean value of each node: " % feature, value_list
			lof,outlier_node_lof,outlier_degree_lof,outlier_value_lof = nlt.lof_detect(value_list,node_list_lof,instances_lof,lof_distance,lof_degree)
			outlier_node_list_lof = []
			outlier_node_value_lof = []
			normal_node_list_lof = []
			normal_node_value_lof = []
			for node_i in outlier_node_lof:
				if node_i in outlier_sim[1:]:
					outlier_node_list_lof.append(node_i)
					outlier_node_value_lof.append(outlier_value_lof[outlier_node_lof.index(node_i)])
				else:
					normal_node_list_lof.append(node_i)
					normal_node_value_lof.append(outlier_value_lof[outlier_node_lof.index(node_i)])
			if outlier_node_list_lof != []:
				print "LOF found that abnormal feature values of abnormal nodes are: ", feature, outlier_node_list_lof, outlier_node_value_lof
			else:
				if normal_node_list_lof != []:
					print "However, LOF found a few anomaly feature values of normal nodes are: ", feature, normal_node_list_lof, normal_node_value_lof
			#print "lof Outlier degree: ", outlier_degree_lof
			nlt.plotFig(instances_lof,lof,feature)
			
			## print results into file
			file = open('file/%s_results.txt' % (stage_id),'a')
			file.write("%s raw mean value of all nodes lof: " % feature+"\r\n")
			file.write(str(value_list_raw)+"\r\n")
			file.write("%s normalized mean value of all nodes lof: " % feature+"\r\n")
			file.write(str(value_list)+"\r\n")
			if outlier_node_list_knn != []:
				file.write("LOF found that abnormal feature values of abnormal nodes are: "+"\r\n")
				file.write(str(feature)+"\r\n")
				file.write(" ".join(outlier_node_list_lof)+"\r\n")
				file.write(str(outlier_node_value_lof)+"\r\n")
			else:
				if normal_node_list_lof != []:
					file.write("However, LOF found a few anomaly feature values of normal nodes are: "+"\r\n")
					file.write(str(feature)+"\r\n")
					file.write(" ".join(normal_node_list_lof)+"\r\n")
					file.write(str(normal_node_value_lof)+"\r\n")
			file.write("lof Outlier degree: "+"\r\n")
			file.write(str(outlier_degree_lof)+"\r\n")
			file.close()
		
		else:
			pass
	
	
	##————————similarity analysis of single node on single feature by relative entropy————————##
	## feature, table and node setting
	bins = re_bins
	feature_list_os = ['cpu_usage', 'ioWaitRatio', 'weighted_io', 'mem_usage', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band'] 
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	node_index_i = 1
	if len(outlier_sim) <= 2:
		print "Less than two abnormal nodes can not calculate relative entropy !"
		
		## print results into file
		file = open('file/%s_results.txt' % (stage_id),'a')
		file.write("Less than two abnormal nodes can not calculate relative entropy !"+"\r\n")
		file.close()
		
	else:
		while (node_index_i<(len(outlier_sim)-1)):
			node_j = outlier_sim[node_index_i]
			node_k = outlier_sim[node_index_i+1]
			for feature in pca_list_pca:
				if feature in feature_list_os:
					table = table_list[0]
					re = nre.node_kl(stage_id,feature,table,node_j,node_k,bins)
					if re > re_threshold:
						print "%s abnormal relative entropy of abnormal node %s and %s is: " % (feature,node_j,node_k),re
						
						## print results into file
						file = open('file/%s_results.txt' % (stage_id),'a')
						file.write("%s abnormal relative entropy of abnormal node %s and %s is: " % (feature,node_j,node_k)+"\r\n")
						file.write(str(re)+"\r\n")
						file.close()
						
					else:
						print "Relative entropy can not find any abnormal %s on any abnormal node !" % feature
					
						## print results into file
						file = open('file/%s_results.txt' % (stage_id),'a')
						file.write("Relative entropy can not find any abnormal %s on any abnormal node !" % feature+"\r\n")
						file.close()
				
				elif feature in feature_list_log:
					table = table_list[1]
					re = nre.node_kl(stage_id,feature,table,node_j,node_k,bins)
					if re > re_threshold:
						print "%s abnormal relative entropy of abnormal node %s and %s is: " % (feature,node_j,node_k),re
						
						## print results into file
						file = open('file/%s_results.txt' % (stage_id),'a')
						file.write("%s abnormal relative entropy of abnormal node %s and %s is: " % (feature,node_j,node_k)+"\r\n")
						file.write(str(re)+"\r\n")
						file.close()
						
					else:
						print "Relative entropy can not find any abnormal %s on any abnormal node !" % feature
						
						## print results into file
						file = open('file/%s_results.txt' % (stage_id),'a')
						file.write("Relative entropy can not find any abnormal %s on any abnormal node !" % feature+"\r\n")
						file.close()
						
				else:
					pass
				
			node_index_i += 1
	
	
	