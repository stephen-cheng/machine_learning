# -*- coding:utf-8 -*-

import pickle as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plimg
from PIL import Image

def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb')as f:
        datadict = p.load(f)
        X = datadict['data']
        Y = datadict['labels']
        X = X.reshape(10000, 3, 32, 32)
        Y = np.array(Y)
        return X, Y

def load_CIFAR_Labels(filename):
    with open(filename, 'rb') as f:
        lines = [x for x in f.readlines()]
        return lines


if __name__ == "__main__":
    labels = load_CIFAR_Labels("../dataset/cifar-10-batches-py/batches.meta")
    print labels[0].encode('utf-8')
    imgX, imgY = load_CIFAR_batch("../dataset/cifar-10-batches-py/data_batch_1")
    print imgX.shape
    print "正在保存图片:"
    for i in xrange(imgX.shape[0]):
        imgs = imgX[i - 1]
        if i < 100:#只循环100张图片,这句注释掉可以便利出所有的图片,图片较多,可能要一定的时间
            img0 = imgs[0]
            img1 = imgs[1]
            img2 = imgs[2]
            i0 = Image.fromarray(img0)
            i1 = Image.fromarray(img1)
            i2 = Image.fromarray(img2)
            img = Image.merge("RGB",(i0,i1,i2))
            name = "img" + str(i)
            img.save("../dataset/cifar-10-images/"+name,"png")#文件夹下是RGB融合后的图像
            '''
            for j in xrange(imgs.shape[0]):
                img = imgs[j - 1]
                name = "img" + str(i) + str(j) + ".png"
                print "正在保存图片" + name
                plimg.imsave("../dataset/cifar-10-image/" + name, img)#文件夹下是RGB分离的图像'''

    print "保存完毕."