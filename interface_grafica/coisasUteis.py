import cv2
import numpy as np
from PIL import Image, ImageGrab
from io import BytesIO
from tkinter import *


#Usem esse arquivo para salvar valores que vocês repetem muito, tipo variaveis, fotos, etc

LARGURA_JANELA, ALTURA_JANELA = 550, 550
DIRETORIO_TRANS_ORIGINAL = r'../data/trans&result/freqOriginal.png'
DIRETORIO_TRANS_EDITADA = r'../data/trans&result/freqEditada.png'

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


#Cria o filtro criado pelo nosso desenho comparando as duas imagens e pegando só a parte q tá desenhada
def cria_filtro_do_desenho(multiplicador_freq):
    imgeditada = cv2.imread(DIRETORIO_TRANS_EDITADA)
    imgOriginal = cv2.imread(DIRETORIO_TRANS_ORIGINAL)
    base = np.ones([300,300])
    #print(f"b:{multiplicador_freq[0]} w:{multiplicador_freq[1]}")
    for x in range(300):
        for y in range (300):
            if not (np.array_equal(imgeditada[x,y], imgOriginal[x,y])):
                if np.array_equal(imgeditada[x,y] , np.array([0,0,0])): #Qd na tela for preto, ela criará uma mascara com um valor entre 0-0.9, vulgo borrachinha da frequencia
                    base[x,y] = multiplicador_freq[0]
                elif np.array_equal(imgeditada[x,y] , np.array([255,255,255])): #Qd na tela for branco, ela  criará a mascara com o multiplicador da frequência passado
                    base[x,y] = multiplicador_freq[1]

    return base


#Tirar isso dps, só salva a imagem editada como um arquivo
