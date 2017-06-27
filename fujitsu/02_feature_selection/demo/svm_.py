'''
SVM classifiers
'''
import load_data as ld
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def svm_(data, target):
	C = 1.0  # svm regularization parameter
	svc = svm.SVC(kernel='linear')
	rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C)
	poly_svc = svm.SVC(kernel='poly', degree=3, C=C)
	lin_svc = svm.LinearSVC(C=C)
	svc_list = [svc, rbf_svc, poly_svc, lin_svc]
	svc_type = ['svc', 'rbf_svc', 'poly_svc', 'lin_svc']
	svm_scores = []
	for clf in svc_list:
		clf.fit(data, target.ravel())
		svm_score = clf.score(feature, target)
		svm_scores.append(svm_score)
	return svm_scores, svc_list, svc_type

def eval_(y_true, y_pred):
	accu = accuracy_score(y_true, y_pred)
	prec = precision_score(y_true, y_pred, average='micro')  
	reca = recall_score(y_true, y_pred, average='micro') 
	f1 = f1_score(y_true, y_pred, average='micro')
	eval_keys = ['accuracy', 'precision', 'recall', 'f1_score']
	eval_values = [accu, prec, reca, f1]
	eval_dict = dict(zip(eval_keys, eval_values))
	return eval_dict
			
if __name__ == '__main__':
	
	n_features = 80
	# train data with svm
	feature = ld.load_data('data/train_set.txt', n_features)
	target = ld.load_data('data/train_targets.txt')
	svm_scores, svc_list, svc_type = svm_(feature, target)
	print 'svm types: ', svc_type
	print 'svm train scores: ', svm_scores
	
	# predict and evaluation
	test_feature = ld.load_data('data/test_set.txt', n_features)
	svm_eval = []
	for svc in svc_list:
		target_predict = svc.predict(test_feature)
		target = ld.load_data('data/test_targets.txt')
		y_true, y_pred = target.ravel(), target_predict.ravel()
		eval_dict = eval_(y_true, y_pred)
		svm_eval.append(eval_dict)
	for i in svm_eval:
		svm_eval_dict = dict(zip(svc_type, svm_eval))
	print svm_eval_dict
	
	


	