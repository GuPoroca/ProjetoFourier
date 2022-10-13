import PySimpleGUI as sg
import cv2

from coisasUteis import  save_graph_as_file, LARGURA_JANELA, ALTURA_JANELA, cria_filtro_do_desenho, DIRETORIO_TRANS_ORIGINAL, DIRETORIO_TRANS_EDITADA
from transformada import inversa_para_imagem, transformada_inversa


# TODO
#   Melhorar UI
#   Adicionar um indicador de cor escolhida
#   Dizer o que a cor faz
#   Adicionar uma barrinha (arrastando) para a pessoa escolher o quanto quer multiplicar esssa frequência


class TelaEdicao:
    # Construtor, java ainda é superior
    def __init__(self, transformada):
        self.transformada = transformada
        # self.imagemoriginal = image.resize((300, 300),Resampling.LANCZOS)  Não precisa mais dar o resize =P
        self.set_atributos()
        self.set_tela_principal()
        self.set_quadro_de_desenho()

    def set_tela_principal(self):
        self.layout = [[sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300),
                                 key="quadro_desenho", pad=(0, 0),
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
                       # [sg.Radio("Pincel preto", "RADIO", enable_events=True, key="ativaP"),
                       # sg.Radio("Pincel branco", "RADIO", enable_events=False, key="ativaB")]

                       ]

        self.telaprincipal = sg.Window("Photoshopee", self.layout, size=(LARGURA_JANELA, ALTURA_JANELA), finalize=True,
                                       element_justification="center")

    def set_quadro_de_desenho(self):
        self.quadro_desenho = self.telaprincipal["quadro_desenho"]  # self.telaprincipal.Element("quadro_desenho")
        self.quadro_desenho.draw_image(filename=DIRETORIO_TRANS_ORIGINAL, location=(0, 300))

    def set_atributos(self):
        self.lastx = None
        self.lasty = None
        self.values = None
        self.event = 'Exit'
        self.tamanho_pincel = 30 # em px
        self.cor_pincel = "black"  # white ou black apenas

    def set_quadro_desenho_binds(self):
        # print("Iniciando quadro de edicao")
        self.quadro_desenho.set_cursor('pencil')
        # Botando as binds no quadro_desenho apenas, antes tava para toda a janela por isso tava bugando
        self.quadro_desenho.Widget.bind('<Button-1>', self.save_pos)
        self.quadro_desenho.Widget.bind("<B1-Motion>", self.pintar)

    def save_pos(self, event):
        self.lastx, self.lasty = event.x, event.y
        # print("Posicao adquirida")
        # print(event)
        # print(event.x, event.y)
        # print(self.lastx, self.lasty)

    def pintar(self, event):
        # print("pintando")

        # self.quadro_desenho.Widget.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.cor_pincel,width=self.tamanho_pincel)

        self.quadro_desenho.draw_rectangle((self.lastx, 300 - self.lasty), (event.x, 300 - event.y),
                                           line_color=self.cor_pincel, line_width=self.tamanho_pincel)

        self.save_pos(event)
        # print(event.x, event.y)
        # print(self.lastx, self.lasty)

    #OBS: gambiarra fudida
    def limpar(self):
        self.quadro_desenho.Widget.delete("all") #Apaga tudo, deixando um quadro em branco
        self.quadro_desenho.draw_image(filename=DIRETORIO_TRANS_ORIGINAL, location=(0, 300)) #Bota imagem de novo


    # pinta as bordas do quadro(fiz isso pra debugar a imagem)
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
        # print("Foto editada salva")
        save_graph_as_file(self.quadro_desenho, DIRETORIO_TRANS_EDITADA)

    # alterna entre branco e preto
    def mudar_cor(self):
        self.cor_pincel = "white" if self.cor_pincel == "black" else "black"

    def run(self) -> None:
        self.set_quadro_desenho_binds()
        while True:  # A brincadeira eh aq
            self.event, self.values = self.telaprincipal.read()

            # Só botar case "a key do botao" e o resultado do clique
            match self.event:
                case 'sairbtn' | sg.WIN_CLOSED:
                    break
                case "corbtn":
                    self.mudar_cor()
                    self.telaprincipal.Element("cortxt").update("Cor atual: " + self.cor_pincel)
                case "salvarbtn":
                    self.salvar()
                    b = cria_filtro_do_desenho(3)
                    resultado(b, self.transformada)
                case "limpabtn":
                    self.limpar()
                case "aumentabtn":
                    self.aumentar_pincel()
                    self.telaprincipal.Element("tamtxt").update("Tamanho do pincel: " + str(self.tamanho_pincel))
                case "diminuibtn":
                    self.diminuir_pincel()
                    self.telaprincipal.Element("tamtxt").update("Tamanho do pincel: " + str(self.tamanho_pincel))

        self.telaprincipal.close()

def resultado(filtro, transformada):
    f_center_filtrado = filtro * transformada;

    img = inversa_para_imagem(transformada_inversa(f_center_filtrado))

    cv2.imwrite("../data/trans&result/resultado.png",img)

# No caso quando integrar com outras telas, terá q remover essa linha e colar a mesma coisa no lugar q a tela será chemada
# TelaEdicao().run()
