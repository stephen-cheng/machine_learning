import numpy as np
import InsertTools
import sys

def KLDistance(p,q):
	if p.any() > 0.000001:
		tp=np.asarray(p,dtype=np.float)
	if q.any() > 0.000001:
		tq=np.asarray(q,dtype=np.float)
	return np.sum(tp*np.log(tp/tq))
	
def node_kl(node1,node2,indexname,tablename,starttime,endtime,bins):
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select %s from %s where node='%s' and timestamp_>=%s and timestamp_<%s;" %(indexname,tablename,node1,starttime,endtime)
	cur.execute(sql)
	rows=cur.fetchall()
	node1_values=[r[0] for r in rows]+list(np.linspace(0,1,bins))
	index_min = min(node1_values)
	index_max = max(node1_values)
	sql="select %s from %s where node='%s' and timestamp_>=%s and timestamp_<%s;" %(indexname,tablename,node2,starttime,endtime)
	cur.execute(sql)
	rows=cur.fetchall()
	node2_values=[r[0] for r in rows]+list(np.linspace(0,1,bins))
	index_min = min(node2_values)
	index_max = max(node2_values)
	node_distribution=np.histogram(node1_values,bins=bins,range=[0,1])[0]
	node1_distribution=np.histogram(node1_values,bins=bins,range=[index_min,index_max])[0]+node_distribution
	node2_distribution=np.histogram(node2_values,bins=bins,range=[index_min,index_max])[0]+node_distribution
	node1_distribution=node1_distribution/float(np.sum(node1_distribution))
	node2_distribution=node2_distribution/float(np.sum(node2_distribution))
	cur.close()
	conn.commit()
	conn.close()
	return KLDistance(node1_distribution,node2_distribution)
	
if __name__=='__main__':
	#min=max=0.0
	#print node_kl("hw004","hw073","cpu_usage","os",1467298880,1467308880,100,0,1)
	#print node_kl("hw004","hw073","cpu_usage","os",1467298880,1467308880,100,min,max)
	r1 = node_kl(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],int(sys.argv[7]))
	r2 = node_kl(sys.argv[2],sys.argv[1],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],int(sys.argv[7]))
	print (r1+r2)/2
