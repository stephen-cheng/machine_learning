"""
This script is for testing ml methods visualization !
"""

import load_data as ld
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
import plot_

if __name__ == '__main__':
	
	feature = ld.load_data('data/train_set.txt')
	target = ld.load_data('data/train_targets.txt')
	feature_test = ld.load_data('data/test_set.txt')
	target_test = ld.load_data('data/test_targets.txt')
	
	# preprocess dataset via pca
	components_num = 3
	feature_reduced, exp_variance_ratio, pca = pca_.pca_(feature, components_num)
	feature_reduced_test, exp_variance_ratio, pca = pca_.pca_(feature_test, components_num)
	feature_new, feature_test_new = feature_reduced[:, :2], feature_reduced_test[:, :2]
	
	# knn 2D visualization i
	clf, clf_score = knn_.knn_(feature_new, target, feature_test_new, target_test)
	title_name = "K Nearest Neighbors Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# svm-linear 2D visualization
	clf, clf_score = svm_linear.svm_(feature_new, target, feature_test_new, target_test)
	title_name = "Linear SVM Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# svm-rbf 2D visualization
	clf, clf_score = svm_rbf.svm_(feature_new, target, feature_test_new, target_test)
	title_name = "SVM-RBF Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# decision tree 2D visualization
	clf, clf_score = dt.dt_(feature_new, target, feature_test_new, target_test)
	title_name = "Decision Tree Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# random forest 2D visualization
	clf, clf_score = rf.rf_(feature_new, target, feature_test_new, target_test)
	title_name = "Random Forest Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# neural networks 2D visualization
	clf, clf_score = nn.nn_(feature_new, target, feature_test_new, target_test)
	title_name = "Neural Networks Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# adaBoost 2D visualization
	clf, clf_score = ada.adab_(feature_new, target, feature_test_new, target_test)
	title_name = "AdaBoost Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# naive bayes 2D visualization
	clf, clf_score = nb.nb_(feature_new, target, feature_test_new, target_test)
	title_name = "Naive Bayes Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	# qda 2D visualization
	clf, clf_score = qda_.qda_(feature_new, target, feature_test_new, target_test)
	title_name = "Quadratic Discirminant Analysis Classifier"
	plot_.plot_(feature_new, target, feature_test_new, target_test, title_name, clf, clf_score)
	
	
	