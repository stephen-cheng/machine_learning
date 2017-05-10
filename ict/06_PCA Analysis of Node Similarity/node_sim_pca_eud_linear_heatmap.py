import InsertTools
import sys
import time
import json 
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib import cm
from matplotlib import axes
	
def nodeSim(app_id,stage_id,weights):
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql = "select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	startTime = int(res[0][0])
	endTime = int(res[0][1])
	
	sql = "select node,avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" % (startTime,endTime)
	cur.execute(sql)
	res = cur.fetchall()
	nodes = {}
	for r in res:
		nodes[r[0]] = list(r[1:])
		
	sql = "select node,avg(ipc),avg(L2_MPKI),avg(L3_MPKI),avg(DTLB_MPKI),avg(ITLB_MPKI),avg(L1I_MPKI),avg(MUL_Ratio) from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 group by node;" % (startTime,endTime)
	cur.execute(sql)
	res = cur.fetchall()
	
	for r in res:
		n = nodes.get(r[0],None)
		if n is None:continue;
		n.extend(list(r[1:]))
    	sim = {}.fromkeys(nodes.keys())
	for k in sim:
		sim[k] = {}.fromkeys(nodes.keys())
		
	for i in nodes:
		for j in nodes:
			sim[i][j] = sim_eud(normalarray(nodes[i],weights),normalarray(nodes[j],weights)) * 1/2 + sim_cos(normalarray(nodes[i],weights),normalarray(nodes[j],weights)) * 1/2
			
	keylist = list()	
	for key in sim.keys():
		keylist.append(key)
	#print keylist
	listemp = ['']
	listemp = listemp + keylist
	
	valuelist = list()
	lst = list()
	for row in sim.values():
		valuelist.append(row)
	for eachvalue in valuelist:
		lists = tuple(eachvalue.values())
		lst.append(lists)
	print lst
	
	draw_heat(listemp,np.array(lst))	
	cur.close()
	conn.commit()
	conn.close()
	return sim
	
def sim_eud(x,y):
	z = 1.0
	return z/(z+np.sqrt(np.sum((x-y)*(x-y))))
	
def sim_cos(a,b):
    return np.sum(a*b)/(np.sqrt(np.sum(a*a))*np.sqrt(np.sum(b*b)))
	
def normalarray(a,weights=None):
	if weights is None:
		w = np.ones(len(a))
	else:w = np.array(weights)
	res = []
	for i in a:
		res.append(float(i))
	return np.array(res) * (1.0/w)
	
def weights():
	conn = InsertTools.getConnection()
	cur = conn.cursor()
	sql = "select submission_time , completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res = cur.fetchall()
	startTime = int(res[0][0])
	endTime = int(res[0][1])
	
	#get max from os
	sql1 = "select max(cpu_usage),max(mem_usage),max(ioWaitRatio),max(weighted_io),max(diskR_band),max(diskW_band) from os where timestamp_ >=%d/1000 and timestamp_ <= %d/1000;" % (startTime,endTime)
	cur.execute(sql1)
	res1 = cur.fetchall()
	r1 = list(res1)
	for each in r1:
		e1 = each

	#get max from log
	sql2 = "select max(ipc),max(L2_MPKI),max(L3_MPKI),max(DTLB_MPKI),max(ITLB_MPKI),max(L1I_MPKI),max(MUL_Ratio) from log where timestamp_ >=%d/1000 and timestamp_ <= %d/1000;" % (startTime,endTime)
	cur.execute(sql2)
	res2 = cur.fetchall()
	r2 = list(res2)
	for each in r2:
		e2 = each
	e = e1 + e2
	return list(e)
	
def draw_heat(xname,data):
	fig = plt.figure(facecolor='w')
	ax1 = fig.add_subplot(2,1,1,position=[0.14,0.08,0.8,0.8])
	ax1.set_xticklabels((xname), range(len(xname)),rotation=0)
	ax1.set_yticklabels((xname), range(len(xname)),rotation=0)
	
	#select the map color
	#cmap = cm.get_cmap('RaYlBu_r', 1000)
	cmap = cm.get_cmap('rainbow', 1000)
	#cmap = cm.get_cmap('spectral', 1000)
	
	#map the colors to data
	map = ax1.imshow(data, interpolation="nearest", cmap=cmap, aspect='auto', vmin=0.0, vmax=1.0)
	cb = plt.colorbar(mappable=map, cax=None, ax=None, shrink=0.6)
	cb.set_label('similarity')
	plt.title(u'Node Similarity Analysis Heatmap')
	plt.savefig('node_sim_pca_eud_linear_heatmap.png')	
	plt.show() 
	
if __name__ == '__main__':
	#app_id = sys.argv[1]
	#stage_id = sys.argv[2]
	app_id = "app-20160719212517-0001"
	stage_id = "spark_stage_app-20160719212517-0001_2"
	weights = weights()
	nodeSim(app_id,stage_id,weights)
	pass
