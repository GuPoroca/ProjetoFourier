import cv2 as cv
import numpy as np



#Função da Transformada
def transformada(imagem):
    image = cv.imread(imagem,0)
    f = np.fft.fft2(image) ##tranformada não centralizada
    f_center = np.fft.fftshift(f) ##transformda centralizada
    return f_center

## função para mostrar transformada como imagem
def transformada_para_imagem(transformada):
    spec = 20 * np.log(np.abs(transformada))
    cv.imwrite("../data/transformadaOriginal.png",spec) #Salva o spectre pra edicao e criacao do filtro (PS: SO VAMOS USAR ISSO PRIMORDIALMENTE PARA VISUALIZACAO E CRIACAO DO FILTRO)
    return spec

def transformada_inversa(trans):
    f_normal =  np.fft.ifftshift(trans) ## reverter centralizaçao
    return np.fft.ifft2(f_normal) ## fazer tranformada inversa

## Função para mostar transformada inversa como imagem
def inversa_para_imagem(inversa):
    return np.abs(inversa)

