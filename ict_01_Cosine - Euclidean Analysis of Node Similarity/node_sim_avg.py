import InsertTools
import sys
import json 
import numpy as np


	

conn=InsertTools.getConnection()
cur=conn.cursor()
sql1="select avg(cpu_usage),avg(mem_usage),avg(ioWaitRatio),avg(weighted_io),avg(diskR_band),avg(diskW_band),avg(netS_band),avg(netR_band) from os"
cur.execute(sql1)
res1=cur.fetchall()
r1=list(res1)
for each in r1:
	e1 = each

sql2="select avg(ipc),avg(L2_MPKI),avg(L3_MPKI),avg(DTLB_MPKI),avg(ITLB_MPKI),avg(L1I_MPKI),avg(MUL_Ratio),avg(DIV_Ratio),avg(FP_Ratio),avg(LOAD_Ratio),avg(STORE_Ratio),avg(BR_Ratio) from log"
cur.execute(sql2)
res2=cur.fetchall()
r2=list(res2)
for each in r2:
	e2 = each
e=e1+e2
print list(e)
	

#nodesy={}
#for r in res2:
#	nodesy[r[0]]=list(r[0:])
#print nodesy[r[0]]
	
