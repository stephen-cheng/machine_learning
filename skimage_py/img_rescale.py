#-*-coding:utf-8-*-

from skimage import transform,data
import matplotlib.pyplot as plt

img = data.camera()
img_r = transform.rescale(img, 0.1)
img_r2 = transform.rescale(img, [0.5,0.25])
img_r3 = transform.rescale(img, 2)

plt.subplot(141)
plt.title('before rescale')
plt.imshow(img, plt.cm.gray)

plt.subplot(142)
plt.title('rescale 0.1')
plt.imshow(img_r)

plt.subplot(143)
plt.title('rescale 0.5*0.25')
plt.imshow(img_r2)

plt.subplot(144)
plt.title('rescale 2')
plt.imshow(img_r3)

plt.show()

print(img.shape)  #图片原始大小 
print(img_r.shape)  #缩小为原来图片大小的0.1倍
print(img_r2.shape)  #缩小为原来图片行数一半，列数四分之一
print(img_r3.shape)   #放大为原来图片大小的2倍

