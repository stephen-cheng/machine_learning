import time
import json 
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib import cm
from matplotlib import axes

xname = ['hw004','hw005','hw006','hw007','hw008','hw009','hw010']
lst = [(1.0000000000000002, 0.074483029449831942, 0.6909737188235221, 0.76661982921130767, 0.74372062847511133, 0.77684241345386862, 0.78473279791108486), (0.074483029449831942, 1.0, -0.3586357017854131, -0.11947187397422541, -0.13324753619850468, -0.1497577637660816, -0.22543260628717676), (0.6909737188235221, -0.3586357017854131, 0.99999999999999978, 0.93803481948810041, 0.91519241219990366, 0.92913581849736848, 0.95325451982097265), (0.76661982921130767, -0.11947187397422541, 0.93803481948810041, 1.0, 0.91882719686302894, 0.97760986759380974, 0.96540706513257879), (0.74372062847511133, -0.13324753619850468, 0.91519241219990366, 0.91882719686302894, 1.0000000000000002, 0.94227148409117401, 0.93474438876751831), (0.77684241345386862, -0.1497577637660816, 0.92913581849736848, 0.97760986759380974, 0.94227148409117401, 1.0000000000000002, 0.98761958708491426), (0.78473279791108486, -0.22543260628717676, 0.95325451982097265, 0.96540706513257879, 0.93474438876751831, 0.98761958708491426, 1.0000000000000002)]
data = np.array(lst)

fig = plt.figure(facecolor='w')
ax1 = fig.add_subplot(1,1,1,position=[0.14,0.08,0.8,0.8])
# ax1.set_xticklabels((xname), fontdict=None,rotation=0)
plt.xticks(range(len(xname)), xname)
plt.yticks(range(len(xname)), xname)
#ax1.set_xticklabels((xname),rotation=0)
#ax1.set_yticklabels((xname),rotation=0)

#select the map color
#cmap = cm.get_cmap('RaYlBu_r', 1000)
cmap = cm.get_cmap('rainbow', 1000)
#cmap = cm.get_cmap('spectral', 1000)

#map the colors to data
map = ax1.imshow(data, interpolation="nearest", cmap=cmap, aspect='auto', vmin=0.0, vmax=1.0)
cb = plt.colorbar(mappable=map, cax=None, ax=None, shrink=0.6)
cb.set_label('similarity')
plt.title(u'Node Similarity Analysis Heatmap')

plt.savefig('node_heatmap.png')	
plt.show() 

