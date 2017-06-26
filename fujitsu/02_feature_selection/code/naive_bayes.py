'''
Naive Bayes Classifier
'''

import load_data as ld
from plot_ import plot_
from sklearn.naive_bayes import GaussianNB

def nb_(feature, target, feature_test, target_test):	
	clf = GaussianNB(priors=None)
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
	
	clf, clf_score = nb_(feature, target, feature_test, target_test)
	print 'naive bayes prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "Naive Bayes classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	
	