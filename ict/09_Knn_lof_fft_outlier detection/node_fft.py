import InsertTools
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, fftshift

def node(stage_id):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	# get app_id
	sql="select app_id, submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	app_id=res[0][0]
	startTime=int(res[0][1])
	endTime=int(res[0][2])
	# get slaves list
	sql="select slaves_list from app where app_id='%s';" %(app_id)
	cur.execute(sql)
	res=cur.fetchall()
	slaves_node=res[0][0]
	node_list = slaves_node.split(',')
	return node_list
	
def node_data(stage_id,feature,table,node):	
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select submission_time, completion_time from stage where stage_id='%s';" %(stage_id)
	cur.execute(sql)
	res=cur.fetchall()
	startTime=int(res[0][0])
	endTime=int(res[0][1])
	sql="select %s from %s where timestamp_ >=%d/1000 and timestamp_ <= %d/1000 and node = '%s';" %(feature,table,startTime,endTime,node)
	cur.execute(sql)
	res=cur.fetchall()
	data_list=[]
	for r in res:
		data = r[0]
		data_list.append(data)
	cur.close()
	conn.commit()
	conn.close()
	return data_list

def fft_plot(data_set,feature,node_list):
	summit_list = []
	color = ['b','g','r','c','m','y','k']
	for i in xrange(len(data_set)):
		# time-domain
		# number of signal points in 
		N = len(data_set[i])
		# time vector
		t = np.arange(0,N,1) 
		y = data_set[i]
		ax = plt.subplot(211)
		ax.plot(t,y, color[i], label=node_list[i])
		ax.set_xlabel('Time')
		ax.set_ylabel('%s-Amplitude' % feature)
		plt.title('node %s fft' % feature)
		# frequency-domain
		# sample spacing
		T = 1.0/100
		x = np.linspace(0.0, N*T, N)
		# fft computing
		yf = fft(y) 
		xf = fftfreq(N, T)
		xf = fftshift(xf)
		yplot = fftshift(yf)
		ax2 = plt.subplot(212)
		summit = max(1.0/N * np.abs(yplot))
		summit_list.append(summit)
		# plotting the spectrum
		ax2.plot(xf,1.0/N * np.abs(yplot),color[i], label=node_list[i]) 
		ax2.set_xlabel('Freq (Hz)')
		ax2.set_ylabel('%s(freq)' % feature)
	plt.legend(loc=0, ncol=1, bbox_to_anchor=(0, 0, 1, 1))
	plt.grid()
	plt.savefig('plot/node_fft_%s.png' % feature)
	#plt.show()
	plt.clf()
	return summit_list

if __name__=='__main__':
	stage_id = sys.argv[1]
	#stage_id = "spark_stage_app-20160630230531-0000_0"
	feature_list_os = ['cpu_usage', 'mem_usage', 'ioWaitRatio', 'weighted_io', 'diskR_band', 'diskW_band', 'netS_band', 'netR_band']
	feature_list_log = ['ipc', 'L2_MPKI', 'L3_MPKI', 'DTLB_MPKI', 'ITLB_MPKI', 'L1I_MPKI', 'MUL_Ratio', 'DIV_Ratio', 'FP_Ratio', 'LOAD_Ratio', 'STORE_Ratio', 'BR_Ratio'] 
	table_list = ['os', 'log']
	node_list = node(stage_id)
	for feature in feature_list_os:
		data_set = []
		table = table_list[0]
		for node in node_list:
			data_list = node_data(stage_id,feature,table,node)
			if data_list != []:
				data_set.append(data_list)
		summit_list = fft_plot(data_set,feature,node_list)
		print "%s Peak Spectral Frequency of %s: " % (feature,node_list),summit_list
	for feature in feature_list_log:
		data_set = []
		table = table_list[1]
		for node in node_list:
			data_list = node_data(stage_id,feature,table,node)
			if data_list != []:
				data_set.append(data_list)
		summit_list = fft_plot(data_set,feature,node_list)
		print "%s Peak Spectral Frequency of %s: " % (feature,node_list),summit_list
	
	