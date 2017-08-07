#-*-coding:utf-8-*-

from skimage import transform,data
import matplotlib.pyplot as plt

img = data.camera()
print(img.shape)  #图片原始大小
img1=transform.rotate(img, 60) #旋转60度，不改变大小 
print(img1.shape)
img2=transform.rotate(img, 30,resize=True)  #旋转30度，同时改变大小
print(img2.shape)   

plt.subplot(121)
plt.title('rotate 60')
plt.imshow(img1,plt.cm.gray)

plt.subplot(122)
plt.title('rotate  30')
plt.imshow(img2,plt.cm.gray)

plt.show()