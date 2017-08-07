#-*-coding:utf-8-*-
import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import skimage
from skimage import io,transform

#===============================python Image==========================================

img = Image.open('dataset/astronaut.png')#打开图片  
plt.imshow(img)
plt.show()

#img.getpixel((height, width))#得到(height, width)处的像素值（可能是一个list，3通道）
img_gray = img.convert("L")#转灰度图  
plt.imshow(img_gray)
plt.show()

size = (64, 64)  
img_resize = img.resize(size, Image.ANTIALIAS)#改变尺寸
plt.imshow(img_resize)
plt.show()

box = (10, 10, 100, 100)  
img_crop = img.crop(box)#在img上的box处截图  
plt.imshow(img_crop)
plt.show()

img_data = np.array(img)  
for i in xrange(300):  
	x = random.randint(0, img_data.shape[0]-1)  
	y = random.randint(0, img_data.shape[1]-1)  
	img_data[x][y][0] = 255  
img_noise = Image.fromarray(img_data)#加300个噪音,转来转去麻烦可以直接用skimage度图片就不用转了  
plt.imshow(img_noise)
plt.show()

img_rotate = img.rotate(90)#图片旋转90
plt.imshow(img_rotate)
plt.show()

img_transpose = img.transpose(Image.FLIP_LEFT_RIGHT)#图片镜像 
plt.imshow(img_transpose)
plt.show()


#==========================================skimage========================================

img_data = io.imread('dataset/astronaut.png')  
img_re = transform.resize(img_data, (64, 64))#改变尺寸  
plt.imshow(img_re)
plt.show()

img_sca = transform.rescale(img_data, 0.25)#缩小/放大图片
plt.imshow(img_sca)
plt.show()

