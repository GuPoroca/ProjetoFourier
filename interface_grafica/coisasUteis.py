import cv2
import numpy as np
from PIL import Image, ImageGrab
from io import BytesIO
from tkinter import *
from matplotlib import pyplot as plt

from interface_grafica.transformada import inversa_para_imagem, transformada_inversa

#Usem esse arquivo para salvar valores que vocês repetem muito, tipo variaveis, fotos, etc

LARGURA_JANELA, ALTURA_JANELA = 550, 550


#Funções suporte
def array_to_data(array):
    im = Image.fromarray(array)
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

def save_graph_as_file(element, filename):
    widget = element.Widget
    x = widget.winfo_rootx() + widget.winfo_x()+4 #Esse 4 foi calculado com precisão suiça, pode confiar
    y = widget.winfo_rooty() + widget.winfo_y() +4
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
    #box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    #grab = ImageGrab.grab(bbox=box)
    #grab.save(filename)



#Filtros de estudo
def filtroPassaBaixa(raio, shapeInexplicavel):
    base = np.zeros(shapeInexplicavel[:2])
    linha, col = shapeInexplicavel[:2]
    centro = (linha / 2, col / 2)
    for x in range(linha):
        for y in range(col):
            if distancia((y, x), centro) < raio:
                base[y, x] = 1
    return base

def filtroPassaAlta(raio, shapeBugante):
    base = np.ones(shapeBugante[:2])
    linha, col = shapeBugante[:2]
    centro = (linha / 2, col / 2)
    for x in range(linha):
        for y in range(col):
            if distancia((y, x), centro) < raio:
                base[y, x] = 0
    return base


def distancia(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def mostrarResultado(pinturamask, transCent):
    transEditCent = pinturamask*transCent; #Sprectre centralizado editado com a nossa edicao
    transEdit = np.fft.ifftshift(transEditCent)
    imagemEditada = np.abs(np.fft.ifft2(transEdit))
    plt.plot(166), plt.imshow(np.abs(imagemEditada), "gray"), plt.title("Processed Image")
    plt.show()
    return imagemEditada


def cria_filtro_do_desenho(multiplicador_freq):
    imgeditada = cv2.imread(r'../data/transformadaEditada.png')
    imgOriginal = cv2.imread(r'../data/transformadaOriginal.png')
    base = np.ones([300,300])
    for x in range(300):
        for y in range (300):
            if not (np.array_equal(imgeditada[x,y], imgOriginal[x,y])):
                if np.array_equal(imgeditada[x,y] , np.array([0,0,0])): #Qd na tela for preto, ela criará uma mascara com 0, vulgo borrachinha da frequencia
                    base[x,y] = 0
                elif np.array_equal(imgeditada[x,y] , np.array([255,255,255])): #Qd na tela for branco, ela  criará a mascara com o multiplicador da frequência passado (SE MUDAR DE COR PARA REPRESENTAR O AUMENTO DE FREQUENCIA, PRECISA MUDAR ESSE 255 AI)
                    # ver como vai fazer quando na multiplicação da mascara com a transformada for maior que 255, possivel tratamento ._.
                    base[x,y] = multiplicador_freq

    return base



def resultado(filtro, transformada):
    print("AG")
    f_center_filtrado = filtro * transformada;

    img = inversa_para_imagem(transformada_inversa(f_center_filtrado))

    cv2.imwrite("../data/FotoEditada.png",img)
