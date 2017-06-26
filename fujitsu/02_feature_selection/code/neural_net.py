'''
Multiple layer Perception Classifier parameters optimization:

	hidden_layer_sizes=(100, ), 
	activation='relu', 
	solver='adam', 
	alpha=0.01, 
	batch_size='auto', 
	learning_rate='constant', 
	learning_rate_init=0.001, 
	power_t=0.5, 
	max_iter=200, 
	shuffle=True, 
	random_state=None, 
	tol=0.0001, 
	verbose=False, 
	warm_start=False, 
	momentum=0.9, 
	nesterovs_momentum=True, 
	early_stopping=False, 
	validation_fraction=0.1, 
	beta_1=0.9, 
	beta_2=0.999
'''

import load_data as ld
from plot_ import plot_
from sklearn.neural_network import MLPClassifier

def nn_(feature, target, feature_test, target_test):	
	clf = MLPClassifier(hidden_layer_sizes=(100, ), activation='relu', 
		solver='adam', alpha=0.01, batch_size='auto', 
		learning_rate='constant', learning_rate_init=0.001, 
		power_t=0.5, max_iter=200, shuffle=True, random_state=None, 
		tol=0.0001, verbose=False, warm_start=False, momentum=0.9, 
		nesterovs_momentum=True, early_stopping=False, 
		validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
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
	
	clf, clf_score = nn_(feature, target, feature_test, target_test)
	print 'neural network prediction accuracy score: ', clf_score
	
	# plot 2D figure
	title_name = "Multiple layer Perception classifier"
	plot_(feature, target, feature_test, target_test, title_name, clf, clf_score)
	
	
	