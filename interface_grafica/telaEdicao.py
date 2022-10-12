import cv2
from PIL import Image
import PySimpleGUI as sg
import numpy as np
from PIL.Image import Resampling #No pycharm isso tá dando erro n sei pq

from coisasUteis import array_to_data, save_graph_as_file, LARGURA_JANELA, ALTURA_JANELA, cria_filtro_do_desenho, \
    resultado
from matplotlib import pyplot as plt

# TODO
#   Função de limpar





class TelaEdicao:
    # Construtor, java ainda é superior
    def __init__(self, transformada):
        self.transformada = transformada
        #self.imagemoriginal = image.resize((300, 300),Resampling.LANCZOS)  Não precisa mais dar o resize =P
        self.set_atributos()
        self.set_tela_principal()
        self.set_quadro_de_desenho()

    def set_tela_principal(self):
        self.layout = [[sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300),
                                 key="quadro_desenho", pad=(0,0),
                                 enable_events=True, background_color="#ffffff", tooltip="Edite aqui", visible=True)],
                       [sg.Text("Botoes quadro")],
                       [sg.Button('Salvar', button_color=("#000000", "#991a1a"), key="salvarbtn"),
                        sg.Exit("Sair", button_color=("#000000", "#991a1a"), key='sairbtn')],
                       [sg.Button("Mudar cor", button_color=("#000000", "#991a1a"), key="corbtn")],
                       [sg.Text("Cor atual: " + self.cor_pincel, key="cortxt")],
                       [sg.Button("Limpar", button_color=("#000000", "#991a1a"), key="limpabtn")],
                       [sg.Button("Aumentar pincel", button_color=("#000000", "#991a1a"), key="aumentabtn"),
                        sg.Button("Diminuir pincel", button_color=("#000000", "#991a1a"), key="diminuibtn")],
                       [sg.Text("Tamanho do pincel: " + str(self.tamanho_pincel), key="tamtxt")],
                       #[sg.Radio("Pincel preto", "RADIO", enable_events=True, key="ativaP"),
                        #sg.Radio("Pincel branco", "RADIO", enable_events=False, key="ativaB")]
                    

                       ]

        self.telaprincipal = sg.Window("Photoshopee", self.layout, size=(LARGURA_JANELA, ALTURA_JANELA), finalize=True,
                                       element_justification="center")

    def set_quadro_de_desenho(self):
        self.quadro_desenho = self.telaprincipal["quadro_desenho"]  # self.telaprincipal.Element("quadro_desenho")
        self.quadro_desenho.draw_image(filename="../data/transformadaOriginal.png", location=(0,300))


    def set_atributos(self):
        self.lastx = None
        self.lasty = None
        self.values = None
        self.event = 'Exit'
        self.tamanho_pincel = 2  # em px
        self.cor_pincel = "white"  # white ou black apenas

    def set_mouse_binds_p_telas(self):
        #print("Iniciando quadro de edicao")
        self.quadro_desenho.set_cursor('pencil')
        self.telaprincipal.TKroot.bind('<Button-1>', self.save_pos)
        self.telaprincipal.TKroot.bind("<B1-Motion>", self.pintar)


    def save_pos(self, event):
        self.lastx, self.lasty = event.x, event.y
        #print("Posicao adquirida")
        #print(event)
        #print(event.x, event.y)
        #print(self.lastx, self.lasty)

    def pintar(self, event):
        #print("pintando")

        self.quadro_desenho.Widget.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.cor_pincel, width=self.tamanho_pincel)
        self.save_pos(event)
        #print(event.x, event.y)
        #print(self.lastx, self.lasty)

    def limpar(self) :
        self.pintarBorda()
        #self.quadro_desenho.delete("all") ---> nao ta funcionando 
        #self.quadro_desenho.Widget.create_line((0, 0, 1000, 1000), fill="white")

    def pintarBorda(self):

        self.quadro_desenho.Widget.create_line((0, 0, 300, 0), fill=self.cor_pincel,
                                                       width=self.tamanho_pincel)
        self.quadro_desenho.Widget.create_line((0, 300, 300, 300), fill=self.cor_pincel,
                                               width=self.tamanho_pincel)
        self.quadro_desenho.Widget.create_line((0, 0, 0, 300), fill=self.cor_pincel,
                                               width=self.tamanho_pincel)
        self.quadro_desenho.Widget.create_line((300, 0, 300, 300), fill=self.cor_pincel,
                                               width=self.tamanho_pincel)
    def aumentar_pincel(self):
        self.tamanho_pincel += 1
        
        
    def diminuir_pincel(self):
        if self.tamanho_pincel > 1:
            self.tamanho_pincel -= 1
        

    def salvar(self):
        #print("Foto editada salva")
        save_graph_as_file(self.quadro_desenho, r'../data/transformadaEditada.png')

    #alterna entre branco e preto
    def mudar_cor(self):
        self.cor_pincel = "white" if self.cor_pincel == "black" else "black"
        
    """    
    def pincel_black(self):
        if self.cor_pincel == "white":
            self.cor_pincel = "black"
            disable = False
        else:
            self.cor_pincel = "black"
            disable = False
        
    def pincel_white(self):
        if self.cor_pincel == "black":
            self.cor_pincel = "white"
            disable = True
        else:
            self.cor_pincel = "white"
            disable = True
    """

    def run(self) -> None:
        self.set_mouse_binds_p_telas()
        while True:  # A brincadeira eh aq
            self.event, self.values = self.telaprincipal.read()


            match self.event:
                case 'sairbtn' : break
                case sg.WIN_CLOSED: break
                case "corbtn":
                    self.mudar_cor()
                    self.telaprincipal.Element("cortxt").update("Cor atual: " + self.cor_pincel)
                case "salvarbtn":
                    self.salvar()
                    b = cria_filtro_do_desenho(1)
                    resultado(b, self.transformada)
                case "limpabtn":
                    self.limpar()
                case "aumentabtn":
                    self.aumentar_pincel()
                    self.telaprincipal.Element("tamtxt").update("Tamanho do pincel: " + str(self.tamanho_pincel))
                case "diminuibtn":
                    self.diminuir_pincel()
                    self.telaprincipal.Element("tamtxt").update("Tamanho do pincel: " + str(self.tamanho_pincel))
                    """
                case "ativaP":
                    self.pincel_black()
                case "ativaB":
                    self.pincel_white()
                """  

                #Só botar case "a key do botao" e o resultado do clique

        self.telaprincipal.close()

#No caso quando integrar com outras telas, terá q remover essa linha e colar a mesma coisa no lugar q a tela será chemada
#TelaEdicao().run()
