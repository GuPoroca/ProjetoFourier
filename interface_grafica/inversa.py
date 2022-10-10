import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from transformada import transformada, transformada_para_imagem

## Recebe imagem e retorna tranformada de fourier inversa dela
def transformada_inversa(imagem):
    f_normal =  np.fft.ifftshift(imagem) ## reverter centralizaçao
    return np.fft.ifft2(f_normal) ## fazer tranformada inversa

## Função para mostar transformada inversa como imagem
def inversa_para_imagem(inversa):
    return np.abs(inversa)

#Teste das Imagens

def teste_das_imagens_inversa():
    img1Path = 'data/pengu.png'
    img2Path = 'data/mario.png'
    img3Path = 'data/zebra.png'
    img4Path = 'data/mulie.png'

    img1 = cv.imread(img1Path,0)
    img2 = cv.imread(img2Path,0)
    img3 = cv.imread(img3Path,0)
    img4 = cv.imread(img4Path,0)

    t1 = transformada(img1Path)
    t2 = transformada(img2Path)
    t3 = transformada(img3Path)
    t4= transformada(img4Path)

    t1inversa = transformada_inversa(t1)
    t2inversa = transformada_inversa(t2)
    t3inversa = transformada_inversa(t3)
    t4inversa = transformada_inversa(t4)

    plt.subplot(421),plt.imshow(transformada_para_imagem(t1), cmap = 'gray')
    plt.title('Imagem transformada'), plt.xticks([]), plt.yticks([])
    plt.subplot(422),plt.imshow( inversa_para_imagem(t1inversa), cmap = 'gray')
    plt.title('Transformada inversa'), plt.xticks([]), plt.yticks([])

    plt.subplot(423),plt.imshow(transformada_para_imagem(t2), cmap = 'gray')
    plt.title('Imagem transformada'), plt.xticks([]), plt.yticks([])
    plt.subplot(424),plt.imshow( inversa_para_imagem(t2inversa), cmap = 'gray')
    plt.title('Transformada inversa'), plt.xticks([]), plt.yticks([])

    plt.subplot(425),plt.imshow(transformada_para_imagem(t3), cmap = 'gray')
    plt.title('Imagem transformada'), plt.xticks([]), plt.yticks([])
    plt.subplot(426),plt.imshow( inversa_para_imagem(t3inversa), cmap = 'gray')
    plt.title('Transformada inversa'), plt.xticks([]), plt.yticks([])

    plt.subplot(427),plt.imshow(transformada_para_imagem(t4), cmap = 'gray')
    plt.title('Imagem transformada'), plt.xticks([]), plt.yticks([])
    plt.subplot(428),plt.imshow(inversa_para_imagem(t4inversa), cmap = 'gray')
    plt.title('Transformada inversa'), plt.xticks([]), plt.yticks([])

    plt.show()

teste_das_imagens_inversa()


