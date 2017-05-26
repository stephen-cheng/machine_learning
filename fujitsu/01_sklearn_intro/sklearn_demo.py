'''
Sample usage of sklearn libaries in machine learning applications
'''

import numpy as np
from sklearn import datasets, svm, neighbors, cluster, decomposition, linear_model
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pylab as pl

# ==============================1.load the dataset=======================================
iris = datasets.load_iris()
print 'shape of iris data: ', iris.data.shape

# target attribute of the dataset
print 'shape of iris\' target:', iris.target.shape
print 'unique type of iris\' target: ', np.unique(iris.target)

# ============================2. learning and predicting by svm===========================
clf = svm.LinearSVC()
clf.fit(iris.data, iris.target)

# have learned from the data, use the model to predict on unseen data
new_data = [ 5.0,  3.6,  1.3,  0.25]
res = clf.predict([new_data])
print 'Linear SVM predict the outcome of target\' type: ', res

# parameters of the model 
print 'parameters of the model: ', clf.coef_

# ==================================3. knn classification=================================
knn = neighbors.KNeighborsClassifier()
knn.fit(iris.data, iris.target) 
new_data2 = [1.1, 2.2, 3.3, 4.4]

# knn assessment and prediction
perm = np.random.permutation(iris.target.size)
iris.data = iris.data[perm]
iris.target = iris.target[perm]
knn.fit(iris.data[:100], iris.target[:100]) 
knn_score = knn.score(iris.data[100:], iris.target[100:]) 
print "knn score: ", "%.4f" % knn_score
r = knn.predict([new_data2])
print 'knn predict the outcome of target\'s type: ', r

# only take the first two features by using a two-dim dataset
X = iris.data[:, :2]  
y = iris.target
n_neighbors = 20

# step size in the mesh
h = .01 

# plot the decision boundary and assign a color to each point 
# in the mesh [x_min, x_max]x[y_min, y_max].
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
	
    # create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)
	
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
	
    # put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
	
    # plot the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xlabel("sepal length")
    plt.ylabel("sepal width")
    plt.title("KNN 3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))
plt.show()

# ================================4. svm classification ===============================
# svm assessment and prediction
C = 1.0  # SVM regularization parameter
svc_lin = svm.SVC(kernel='linear', C=C)
svc_poly = svm.SVC(kernel='poly', degree=3, C=C)
svc_rbf = svm.SVC(kernel='rbf', gamma=0.7, C=C)

svc_lin.fit(iris.data[:100], iris.target[:100])
svc_poly.fit(iris.data[:100], iris.target[:100])
svc_rbf.fit(iris.data[:100], iris.target[:100])
 
lin_score = svc_lin.score(iris.data[100:], iris.target[100:])
poly_score = svc_poly.score(iris.data[100:], iris.target[100:])
rbf_score = svc_rbf.score(iris.data[100:], iris.target[100:])
 
print "svm-linear score: ", "%.4f" % lin_score
print "svm-poly score: ", "%.4f" % poly_score
print "svm-rbf score: ", "%.4f" % rbf_score

r_lin = svc_lin.predict([new_data2])
r_poly = svc_poly.predict([new_data2])
r_rbf = svc_rbf.predict([new_data2])

print 'svm-linear predict the outcome of target\'s type: ', r_lin
print 'svm-poly predict the outcome of target\'s type: ', r_poly
print 'svm-rbf predict the outcome of target\'s type: ', r_rbf

# plot SVM
svc_lin = svm.SVC(kernel='linear', C=C).fit(X, y)
svc_poly = svm.SVC(kernel='poly', degree=3, C=C).fit(X, y)
svc_rbf = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, y)

# title for the plots
titles = ['SVC with linear kernel',
          'SVC with polynomial (degree 3) kernel',
		  'SVC with RBF kernel']

for i, clf in enumerate((svc_lin, svc_poly, svc_rbf)):
    # Plot the decision boundary. For that, we will assign a color to each
    plt.subplot(3, 1, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])
plt.show()

# ====================================5. Kmeans clustering========================================
k_means = cluster.KMeans(n_clusters=3)
k_means.fit(iris.data) 
labels = k_means.labels_
print('Kmeans clustering labels: ', labels[::10])
#[1 1 1 1 2 2 1 0 2 0 1 1 2 2 2]
print('raw labels: ', iris.target[::10])
#[0 0 0 0 1 1 0 2 1 2 0 0 2 2 1]

# Kmeans clustering 3D plot
np.random.seed(5)

centers = [[1, 1], [-1, -1], [1, -1]]
X = iris.data
y = iris.target

fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
plt.cla()
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=labels.astype(np.float))

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')

# Plot the ground truth
fig = plt.figure(1, figsize=(3, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
plt.cla()

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean() + 1.5,
              X[y == label, 2].mean(), name,
              horizontalalignment='center',
              bbox=dict(alpha=.6, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 2, 0]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y)

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title("Kmean 3 clusters")
plt.show()

# ================================================6. PCA==============================================
pca = decomposition.PCA(n_components=2)
pca.fit(iris.data)
X = pca.transform(iris.data)

# PCA plot
pl.scatter(X[:, 0], X[:, 1], c=iris.target)
pl.title('PCA Plot')
pl.show()

# =============================7. Linear model: from regression to sparsity==========================
# lodad diabetes
diabetes = datasets.load_diabetes()
diabetes_X_train = diabetes.data[:-20]
diabetes_X_test  = diabetes.data[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test  = diabetes.target[-20:]

# lasso regression 
regr = linear_model.Lasso(alpha=.3)
regr.fit(diabetes_X_train, diabetes_y_train)
#print regr.coef_
regr_score = regr.score(diabetes_X_test, diabetes_y_test)
print 'lasso regression score: ', regr_score

# linear regression
lin = linear_model.LinearRegression()
lin.fit(diabetes_X_train, diabetes_y_train) 
lin_score = lin.score(diabetes_X_test, diabetes_y_test) 
print 'linear regression score: ', lin_score

# Use only one feature for plotting
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)
lin.fit(diabetes_X_train, diabetes_y_train)

# Plot lasso outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='red')
plt.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.title("Lasso Regression")
plt.show()

# Plot linear outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='red')
plt.plot(diabetes_X_test, lin.predict(diabetes_X_test), color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.title("Linear Regression")
plt.show()


