import xml.etree.ElementTree as ET

if __name__=='__main__':
	et=ET.parse("node_sim_config.xml")
	root=et.getroot()
	sim_threshold=float(root.findtext("sim_threshold"))
	k_kmeans=int(root.findtext("k_kmeans"))
	dis_knn=float(root.findtext("dis_knn"))
	lof_distance=float(root.findtext("lof_distance"))
	lof_degree=float(root.findtext("lof_degree"))
	re_bins=int(root.findtext("re_bins"))
	print sim_threshold,k_kmeans,dis_knn,lof_distance,lof_degree,re_bins