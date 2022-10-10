import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#Função da Transformada
def transformada(imagem):
    image = cv.imread(imagem,0)
    f = np.fft.fft2(image) ##tranformada não centralizada
    f_center = np.fft.fftshift(f) ##transformda centralizada
    return f_center
    
## função para mostrar transformada como imagem
def transformada_para_imagem(transformada):
    return 20*np.log(np.abs(transformada))

#Teste das Imagens

def teste_das_imagens():   
    img1Path = '../data/pengu.png'
    img2Path = '../data/mario.png'
    img3Path = '../data/zebra.png'
    img4Path = '../data/mulie.png'

    img1 = cv.imread(img1Path,0)
    img2 = cv.imread(img2Path,0)
    img3 = cv.imread(img3Path,0)
    img4 = cv.imread(img4Path,0)

    t1 = transformada(img1Path)
    t2 = transformada(img2Path)
    t3 = transformada(img3Path)
    t4= transformada(img4Path)

    plt.subplot(421),plt.imshow(img1, cmap = 'gray')
    plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(422),plt.imshow( transformada_para_imagem(t1), cmap = 'gray')
    plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

    plt.subplot(423),plt.imshow(img2, cmap = 'gray')
    plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(424),plt.imshow( transformada_para_imagem(t2), cmap = 'gray')
    plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

    plt.subplot(425),plt.imshow(img3, cmap = 'gray')
    plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(426),plt.imshow( transformada_para_imagem(t3), cmap = 'gray')
    plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

    plt.subplot(427),plt.imshow(img4, cmap = 'gray')
    plt.title('Imagem Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(428),plt.imshow(transformada_para_imagem(t4), cmap = 'gray')
    plt.title('Transformada da Imagem'), plt.xticks([]), plt.yticks([])

    plt.show()

##teste_das_imagens()


