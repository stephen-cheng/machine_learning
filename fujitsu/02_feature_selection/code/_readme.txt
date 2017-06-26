Programming Script Execution Flow Description:

1) load data
	input:	python load_data.py 
	output:	matrix of raw data (rows * features)

2) PCA
	input:	python pca_.py
	ouput:	explained variance ratio, e.g., [ 0.76057087  0.19704174  0.02280473  0.00820668  0.00489209] 
			confidence interval, e.g., 0.993516107874
			pca features index, e.g., [83, 41, 39, 64, 66]
			2D & 3D reduced feature plot
			
3) ML Classification
	input:	python knn_.py
			python svm_linear.py
			python svm_rbf.py
			python decision_three.py
			python random_forest.py
			python neural_net.py
			python adaboost_.py
			python naive_bayes.py
			python qda_.py		
	output:	accuracy, e.g., 0.448640483384
			2D classification figure
			
4) others
	input: 	python test_assess.py
	output:	all ml classification assessment
	
	write_data.py is to write the reduced data after pca processing into the file.
	data directory is the placement of data file 
	results directory is to save the plot


