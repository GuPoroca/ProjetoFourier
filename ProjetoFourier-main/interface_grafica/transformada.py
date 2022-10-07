import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


#Função da Transformada
def transformada(imagem):
    f = np.fft.fft2(imagem)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    return magnitude_spectrum


#Teste das Imagens

# img1 = cv.imread('data/pengu.png',0)
# img2 = cv.imread('data/mario.png',0)
# img3 = cv.imread('data/zebra.png',0)
# img4 = cv.imread('data/mulie.png',0)

# t1 = transformada(img1)
# t2 = transformada(img2)
# t3 = transformada(img3)
# t4= transformada(img4)

# plt.subplot(421),plt.imshow(img1, cmap = 'gray')
# plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(422),plt.imshow(t1, cmap = 'gray')
# plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

# plt.subplot(423),plt.imshow(img2, cmap = 'gray')
# plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(424),plt.imshow(t2, cmap = 'gray')
# plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

# plt.subplot(425),plt.imshow(img3, cmap = 'gray')
# plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(426),plt.imshow(t3, cmap = 'gray')
# plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

# plt.subplot(427),plt.imshow(img4, cmap = 'gray')
# plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(428),plt.imshow(t4, cmap = 'gray')
# plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

# plt.show()




