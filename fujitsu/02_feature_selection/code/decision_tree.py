'''
DecisionTree Classifier parameters optimization:

	max_depth=None, 
	min_samples_split=2, 
	min_samples_leaf=1, 
	min_weight_fraction_leaf=0.0, 
	max_features=None, 
	random_state=None, 
	max_leaf_nodes=None
	
'''

import load_data as ld
from plot_ import plot_
from sklearn.tree import DecisionTreeClassifier

def dt_(feature, target, feature_test, target_test):	
	clf = DecisionTreeClassifier(criterion='gini', splitter='best', 
		max_depth=5, min_samples_split=2, min_samples_leaf=1, 
		min_weight_fraction_leaf=0.0, max_features=None, 
		random_state=None, max_leaf_nodes=None, min_impurity_split=1e-07, 
		class_weight=None, presort=False)
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
	
	clf, clf_score = dt_(feature, target, feature_test, target_test)
	print 'decision tree prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "DecisionTree classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	