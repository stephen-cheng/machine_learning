'''
Random Forest Classifier parameters optimization:

	n_estimators=10, 
	criterion='gini', 
	max_depth=5, 
	min_samples_split=2, 
	min_samples_leaf=1, 
	min_weight_fraction_leaf=0.0, 
	max_features='auto', 
	max_leaf_nodes=None, 
	min_impurity_split=1, 
	bootstrap=True, 
	oob_score=False, 
	n_jobs=1, 
	verbose=0
'''

import load_data as ld
from plot_ import plot_
from sklearn.ensemble import RandomForestClassifier

def rf_(feature, target, feature_test, target_test):	
	clf = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=5, 
								 min_samples_split=2, min_samples_leaf=1, 
								 min_weight_fraction_leaf=0.0, max_features='auto', 
								 max_leaf_nodes=None, min_impurity_split=1, bootstrap=True, 
								 oob_score=False, n_jobs=1, random_state=None, 
								 verbose=0, warm_start=False, class_weight=None)
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
	
	clf, clf_score = rf_(feature, target, feature_test, target_test)
	print 'random forest prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "Random Forest classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	
	