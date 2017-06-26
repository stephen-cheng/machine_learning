'''
KNeighbors classifiers parameters optimization:

	n_neighbors=3, 
	weights='uniform', 
	algorithm='auto', 
	leaf_size=30, 
	p=2
'''

import load_data as ld
from plot_ import plot_
from sklearn.neighbors import KNeighborsClassifier


def knn_(feature, target, feature_test, target_test):
	clf = KNeighborsClassifier(n_neighbors=3, weights='uniform', 
		algorithm='auto', leaf_size=30, p=2, metric='minkowski', 
		metric_params=None, n_jobs=1)
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
	
	clf, clf_score = knn_(feature, target, feature_test, target_test)
	print 'knn prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "K Nearest Neighbors"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	