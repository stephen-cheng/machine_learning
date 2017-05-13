from math import sqrt
import InsertTools
import sys
import time
import numpy as np

class IndexPearson(object):
	def __init__(self, stage_id):
		self.stage_id = stage_id
	
	def node_index(self, index1, index2):
		conn = InsertTools.getConnection()
		cur = conn.cursor()
		sql = "select submission_time, completion_time from stage where stage_id='%s';" % (self.stage_id)
		cur.execute(sql)
		res = cur.fetchall()
		startTime = int(res[0][0])
		endTime = int(res[0][1])
		index1_list, node1_list = self.index_table(index1, startTime, endTime)
		index2_list, node2_list = self.index_table(index2, startTime, endTime)
		cur.close()
		conn.commit()
		conn.close
		if len(index1_list) != len(index2_list):
			minLen = min(len(index1_list), len(index2_list))
			index1_list = index1_list[:minLen]
			index2_list = index2_list[:minLen]
			node1_list = node1_list[:minLen]
			node2_list = node2_list[:minLen]
		return index1_list, index2_list, node1_list, node2_list
		
	def index_table(self, index, startTime, endTime):
		os_list = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 
			'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
		log_list = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 
			'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio']
		conn = InsertTools.getConnection()
		cur = conn.cursor()
		if index in os_list:
			sql = "select node, %s from os where timestamp_ >= %d / 1000 and timestamp_ <= %d / 1000;" \
				% (index, startTime, endTime) 
		elif index in log_list:
			sql = "select node, %s from log where timestamp_ >= %d / 1000 and timestamp_ <= %d / 1000;" \
				% (index, startTime, endTime) 
		else: pass
		cur.execute(sql)
		res = cur.fetchall()
		node_list = []
		index_list = []
		for r in res:
			node_list.append(r[0])
			index_list.append(r[1])
		cur.close()
		conn.commit()
		conn.close
		return index_list, node_list

	def multiply(self, a, b):
		sum_ab = 0.0
		for i in range(len(a)):
			temp = a[i] * b[i]
			sum_ab += temp
		return sum_ab

	def pearson(self, x, y):
		n = len(x)
		sum_x = sum(x)
		sum_y = sum(y)
		sum_xy = self.multiply(x, y)
		sum_x2 = sum([pow(i, 2) for i in x])
		sum_y2 = sum([pow(j, 2) for j in y])
		molecular = sum_xy - (float(sum_x) * float(sum_y) / n)
		denominator = sqrt((sum_x2 - float(sum_x**2) / n) * (sum_y2 - float(sum_y**2) / n))
		return molecular / denominator

if __name__=='__main__':
	stage_id = sys.argv[1]
	index1 = sys.argv[2]
	index2 = sys.argv[3]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	myStage = IndexPearson(stage_id)
	dataX, dataY, nodeX, nodeY = myStage.node_index(index1, index2)
	myPearson = myStage.pearson(dataX, dataY)
	print 'Pearson of [%s] and [%s]: ' % (index1, index2), myPearson
	
