#-*-coding:utf-8-*-
from scipy.misc import imsave
import numpy as np
import cPickle


# 解压缩，返回解压后的字典
def unpickle(file):
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

# 生成训练集图片，如果需要png格式，只需要改图片后缀名即可。
for j in range(1, 6):
    dataName = "../dataset/cifar-10-batches-py/data_batch_" + str(j)  # 读取当前目录下的data_batch12345文件。
    Xtr = unpickle(dataName)
    print Xtr
    print dataName + " is loading..."

    for i in range(0, 10000):
        img = np.reshape(Xtr['data'][i], (3, 32, 32))  # Xtr['data']为图片二进制数据
        img = img.transpose(1, 2, 0)  # 读取image
        picName = '../dataset/cifar-10-img/img_train/' + str(Xtr['labels'][i]) + '_' + str(i + (j - 1)*10000) + '.jpg'  # Xtr['labels']为图片的标签，值范围0-9。
        imsave(picName, img)
    print dataName + " loaded."

print "test_batch is loading..."

# 生成测试集图片
testXtr = unpickle("../dataset/cifar-10-batches-py/test_batch")
for i in range(0, 10000):
    img = np.reshape(testXtr['data'][i], (3, 32, 32))
    img = img.transpose(1, 2, 0)
    picName = '../dataset/cifar-10-img/img_test/' + str(testXtr['labels'][i]) + '_' + str(i) + '.jpg'
    imsave(picName, img)
print "test_batch loaded."