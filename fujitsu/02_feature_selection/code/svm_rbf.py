'''
SVM-rbf classifier parameters optimization:
	
	C=1.0, 
	kernel='rbf', 
	degree=3, 
	gamma=2.0, 
	coef0=0.0, 
	shrinking=True, 
	probability=False, 
	tol=0.001, 
	cache_size=200, 
	class_weight=None, 
	verbose=False, 
	max_iter=-1
'''

import load_data as ld
from plot_ import plot_
from sklearn import svm

def svm_(feature, target, feature_test, target_test):
	# C: svm regularization parameter
	clf = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=2, 
		coef0=0.0, shrinking=True, probability=False, 
		tol=0.001, cache_size=200, class_weight=None, 
		verbose=False, max_iter=-1, decision_function_shape=None, 
		random_state=None)
	clf.fit(feature, target.ravel())
	clf_score = clf.score(feature_test, target_test)
	clf_predict = clf.predict(feature_test)
	return clf, clf_score
			
if __name__ == '__main__':
	
	# predict and evaluation 
	feature = ld.load_data('data/train_set.txt')
	target = ld.load_data('data/train_targets.txt')
	feature_test = ld.load_data('data/test_set.txt')
	target_test = ld.load_data('data/test_targets.txt')
	
	feature, feature_test = feature[:, :2], feature_test[:, :2]
	
	clf, clf_score = svm_(feature, target, feature_test, target_test)
	print 'svm-rbf prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "SVM-RBF classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	
	
	
	