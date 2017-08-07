from skimage import transform,data
import matplotlib.pyplot as plt
import skimage

#img = data.camera()
img = skimage.io.imread('dataset/0_11.jpg')
dst=transform.resize(img, (256, 256))

skimage.io.imsave('dataset_p/0_11_p.png', dst)

plt.subplot(121)
plt.title('before resize')
plt.imshow(img, plt.cm.gray)

plt.subplot(122)
plt.title('after resize')
plt.imshow(dst, plt.cm.gray)

plt.show()
