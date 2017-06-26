"""
This script is for testing ml methods evaluation !
"""

import load_data as ld
import write_data as wd
import pca_
import knn_
import svm_rbf
import svm_linear
import decision_tree as dt
import random_forest as rf
import neural_net as nn
import adaboost_ as ada
import naive_bayes as nb
import qda_

if __name__ == '__main__':
	
	# load data
	feature = ld.load_data('data/train_set.txt', n_features=None)
	target = ld.load_data('data/train_targets.txt')
	feature_test = ld.load_data('data/test_set.txt', n_features=None)
	target_test = ld.load_data('data/test_targets.txt')
	
	# pca
	components_num = 5
	feature_reduced, exp_variance_ratio, pca = pca_.pca_(feature, components_num)
	print('train explained variance ratio (first %d components): %s'
		  % (components_num, str(exp_variance_ratio)))
	print ('confidence interval: %s' % (str(exp_variance_ratio.sum())))
	feature_reduced_test, exp_variance_ratio_test, pca_test = pca_.pca_(feature_test, components_num)
	print('test explained variance ratio (first %d components): %s'
		  % (components_num, str(exp_variance_ratio_test)))
	print ('confidence interval: %s' % (str(exp_variance_ratio_test.sum())))
	
	# data reduced write to file
	wd.write_data('data/train_set_pca.txt', feature_reduced)
	wd.write_data('data/test_set_pca.txt', feature_reduced_test)
	
	# pca index
	pca_index = pca_.pca_index(feature, components_num)
	print "pca feature index: ", pca_index
	
	# pca plot
	pca_.pca_plot(pca)
	#pca_.pca_scatter(feature_reduced, target.ravel())
	#pca_.pca_plot(pca_test)
	pca_.pca_scatter(feature_reduced_test, target_test.ravel())
	
	# knn evaluation
	clf, clf_score = knn_.knn_(feature_reduced, target, feature_reduced_test, target_test)
	print "knn prediction accuracy score: ", clf_score
	
	# svm-linear evaluation 
	clf, clf_score = svm_linear.svm_(feature_reduced, target, feature_reduced_test, target_test)
	print "svm-linear prediction accuracy score: ", clf_score
	
	# svm-rbf evaluation
	clf, clf_score = svm_rbf.svm_(feature_reduced, target, feature_reduced_test, target_test)
	print "svm-rbf prediction accuracy score: ", clf_score
	
	# decision tree evaluation 
	clf, clf_score = dt.dt_(feature_reduced, target, feature_reduced_test, target_test)
	print "decision tree prediction accuracy score: ", clf_score
	
	# random forest evaluation 
	clf, clf_score = rf.rf_(feature_reduced, target, feature_reduced_test, target_test)
	print "random forest prediction accuracy score: ", clf_score
	
	# neural networks evaluation
	clf, clf_score = nn.nn_(feature_reduced, target, feature_reduced_test, target_test)
	print "neural networks prediction accuracy score: ", clf_score

	# adaBoost evaluation
	clf, clf_score = ada.adab_(feature_reduced, target, feature_reduced_test, target_test)
	print "adaBoost prediction accuracy score: ", clf_score
        
	# naive bayes evaluation
	clf, clf_score = nb.nb_(feature_reduced, target, feature_reduced_test, target_test)
	print "naive bayes prediction accuracy score: ", clf_score
	
	# qda evaluation
	clf, clf_score = qda_.qda_(feature_reduced, target, feature_reduced_test, target_test)
	print "quadratic discriminant analysis prediction accuracy score: ", clf_score
	
	
	
	