'''
Gaussian Process Classifier
'''

import load_data as ld
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

def gauss_(feature, target, feature_test, target_test):	
	clf = GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True)
	clf.fit(feature, target.ravel())
	clf_score = clf.score(feature_test, target_test)
	clf_predict = clf.predict(feature_test)
	return clf_score
			
if __name__ == '__main__':
	
	# predict and evaluation 
	feature = ld.load_data('data/train_set.txt')
	target = ld.load_data('data/train_targets.txt')
	feature_test = ld.load_data('data/test_set.txt')
	target_test = ld.load_data('data/test_targets.txt')
	clf_score = gauss_(feature, target, feature_test, target_test)
	print 'gaussian process prediction accuracy score: ', clf_score
	
	
	