import kNN
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# easy try
group, labels = kNN.createDataSet()
predict = kNN.classify0([0,0], group, labels, 3)
print(predict)

# load data
datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')
print(datingDataMat)
print(datingLabels[0:20])

# scatter plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0], datingDataMat[:,1],
  15.0*np.array(datingLabels), 15.0*np.array(datingLabels))
plt.show()

# normalization
normMat, ranges, minVals = kNN.autoNorm(datingDataMat)
print(normMat)
print(ranges)
print(minVals)

# test error rate
kNN.datingClassTest()

# predict
kNN.classifyPerson()

# handwriting nums recognition
# load daata
testVector = kNN.img2vector('dataset/testDigits/0_13.txt')
print(testVector[0, 0:31])

# handwriting class test 
kNN.handwritingClassTest()

