from PIL import Image
import PySimpleGUI as sg
import numpy as np
from PIL.Image import Resampling #No pycharm isso tá dando erro n sei pq

from coisasUteis import array_to_data, save_element_as_file, LARGURA_JANELA, ALTURA_JANELA


# TODO
#   Adicionar botões de  aumentar/diminuir pincel,limpar e integrar com as outras telas :Franciele





class TelaEdicao:
    # Construtor, java ainda é superior
    def __init__(self, image):
        image = Image.fromarray(image)
        self.imagemoriginal = image.resize((300, 300),Resampling.LANCZOS)  # Abre a imagem e da resize
        self.set_atributos()
        self.setTelaPrincipal()
        self.setQuadroDeDesenho()

    def setTelaPrincipal(self):
        self.layout = [[sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300),
                                 key="quadro_desenho",
                                 change_submits=True, background_color="#ffffff", tooltip="Edite aqui", visible=True,
                                 pad=(5, 5))],
                       [sg.Text("Botoes quadro")],
                       [sg.Button('Salvar', button_color=("#000000", "#991a1a"), key="salvarbtn"),
                        sg.Exit("Sair", button_color=("#000000", "#991a1a"), key='sairbtn')],
                       [sg.Button("Mudar cor", button_color=("#000000", "#991a1a"), key="corbtn")]

                       ]

        self.telaprincipal = sg.Window("Photoshopee", self.layout, size=(LARGURA_JANELA, ALTURA_JANELA), finalize=True,
                                       element_justification="center")
    def setQuadroDeDesenho(self):
        data = array_to_data(np.array(self.imagemoriginal,
                                      dtype=np.uint8))  # Transforma a imagem em uma array de dados no formato uint8 e da array converte para os dados no formato necessário para botar no canvas

        self.quadro_desenho = self.telaprincipal["quadro_desenho"]  # self.telaprincipal.Element("quadro_desenho")
        self.quadro_desenho.draw_image(data=data, location=(0, 300))

    def set_atributos(self):
        self.lastx = None
        self.lasty = None
        self.values = None
        self.event = 'Exit'
        self.tamanho_pincel = 2  # em px
        self.cor_pincel = "white"  # white ou black apenas

    def set_mouse_binds_p_telas(self):
        print("Iniciando quadro de edicao")
        self.quadro_desenho.set_cursor('pencil')
        self.telaprincipal.TKroot.bind('<Button-1>', self.save_pos)
        self.telaprincipal.TKroot.bind("<B1-Motion>", self.pintar)
    def save_pos(self, event):
        self.lastx, self.lasty = event.x, event.y
        print("Posicao adquirida")
        print(event)
        print(event.x, event.y)
        print(self.lastx, self.lasty)

    def pintar(self, event):
        print("pintando")
        self.quadro_desenho.Widget.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.cor_pincel, width=self.tamanho_pincel)
        self.save_pos(event)
        print(event.x, event.y)
        print(self.lastx, self.lasty)

    def limpar(self) :
        pass

    def aumentar_pincel(self):
        pass
    def diminuir_pincel(self):
        pass

    def salvar(self):
        print("Foto editada salva")
        save_element_as_file(self.quadro_desenho, r'__pycache__/imagem_editada.png')

    #alterna entre branco e preto
    def mudar_cor(self):
        self.cor_pincel = "white" if self.cor_pincel == "black" else "black"

    def run(self) -> None:
        self.set_mouse_binds_p_telas()
        while True:  # A brincadeira eh aq
            self.event, self.values = self.telaprincipal.read()

            match self.event:
                case 'sairbtn' : break
                case sg.WIN_CLOSED: break
                case "corbtn":
                    self.mudar_cor()
                case "salvarbtn":
                    self.salvar()

                #Só botar case "a key do botao" e o resultado do clique

        self.telaprincipal.close()

#No caso quando integrar com outras telas, terá q remover essa linha e colar a mesma coisa no lugar q a tela será chemada
#TelaEdicao().run()
