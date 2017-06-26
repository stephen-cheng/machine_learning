'''
 Quadratic Discriminant Analysis Classifier parameters optimization:
 
	reg_param=0.0, 
	store_covariances=False, 
	tol=0.000 
'''

import load_data as ld
from plot_ import plot_
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

def qda_(feature, target, feature_test, target_test):	
	clf = QuadraticDiscriminantAnalysis(priors=None, reg_param=0.0, 
										store_covariances=False, tol=0.0001)
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
	
	clf, clf_score = qda_(feature, target, feature_test, target_test)
	print 'quadratic discriminant prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "Quadratic Discriminant Analysis classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	