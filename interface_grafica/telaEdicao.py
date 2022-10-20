import PySimpleGUI as sg
import cv2

from coisasUteis import save_graph_as_file, LARGURA_JANELA, ALTURA_JANELA, cria_filtro_do_desenho, \
    DIRETORIO_TRANS_ORIGINAL, DIRETORIO_TRANS_EDITADA
from transformada import inversa_para_imagem, transformada_inversa

# TODO
#   Melhorar UI, ainda preciso

class TelaEdicao:
    # Construtor, java ainda é superior
    def __init__(self, transformada):
        self.transformada = transformada
        self.multiplicadorFreq = [0.0, 1.0]  # multiplicadores para o preto([0]) e branco([1])
        self.set_atributos()
        self.set_tela_principal()
        self.set_quadro_de_desenho()

    def set_tela_principal(self):
        btnsair = [sg.Exit("Sair", button_color=("#000000", "#991a1a"), key='sairbtn')]
        tam = [[sg.Button("+", button_color=("#000000", "#991a1a"), key="aumentabtn", size=(1, 1))],
               [sg.Text(f'{self.tamanho_pincel} px' ,key="tamtxt", pad=(5, 5))],
               [sg.Button("-", button_color=("#000000", "#991a1a"), key="diminuibtn", size=(1, 1))]]

        slider = [sg.Slider((0, 0.9), resolution=.1, default_value=0.0, size=(5, 20), enable_events=True,
                            orientation='horizontal', expand_x=True, key='freqslider')]
        layout = [
            [sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300),
                      key="quadro_desenho", pad=(0, 0),
                      enable_events=True, background_color="#ffffff", tooltip="Edite aqui", visible=True)]
        ]

        layout_frame1 = [
            [sg.Frame("Tamanho Pincel", layout=tam, pad=(5, 3), title_location=sg.TITLE_LOCATION_TOP,
                      element_justification='center', expand_x=True, expand_y=True)
                , sg.Frame('Ferramentas', title_location=sg.TITLE_LOCATION_TOP, layout=[[sg.Frame("", layout=[
                [sg.Button("Cor", expand_x=True, button_color=("#FFFFFF", "#000000"), key="corbtn")],
                [sg.Button("Borracha", expand_x=True, button_color=("#000000", "#991a1a"), key="borrachabtn")],
                [sg.Button("Limpar", expand_x=True, button_color=("#000000", "#991a1a"), key="limpabtn")]])]])],
            [sg.Frame("Arquivo", [[sg.Button("Sair", expand_x=True ,button_color=("#000000", "#991a1a"), key='sairbtn'),
                                   sg.Button('Salvar', expand_x=True, button_color=("#000000", "#ffb077"),
                                             key="salvarbtn")]], pad=(5, 3),
                      expand_x=True, expand_y=True,
                      title_location=sg.TITLE_LOCATION_TOP)],
        ]

        layout_frame2 = [slider, [sg.Text(f"Diminuindo frequencias", key='textslider')],
                         [sg.Frame(title="Valores",
                                   layout=[[sg.Text(f"Preto: {self.multiplicadorFreq[0]}", key="valoresPreto")],
                                           [sg.Text(f"Branco: {self.multiplicadorFreq[0]}", key="valoresBranco")]])]]

        layout += [
            [sg.Frame("", layout_frame1, size=(280, 250)),
             sg.Frame("Multiplicador de frequência", layout_frame2, size=(200, 250),
                      title_location=sg.TITLE_LOCATION_TOP)], ]

        self.telaprincipal = sg.Window("Photoshopee", layout, margins=(0, 0), size=(LARGURA_JANELA, ALTURA_JANELA),
                                       finalize=True,
                                       element_justification="center")

    def set_quadro_de_desenho(self):
        self.quadro_desenho = self.telaprincipal["quadro_desenho"]  # self.telaprincipal.Element("quadro_desenho")
        self.quadro_desenho.draw_image(filename=DIRETORIO_TRANS_ORIGINAL, location=(0, 300))

    def set_atributos(self):
        self.lastx = None
        self.lasty = None
        self.values = None
        self.event = 'Exit'
        self.tamanho_pincel = 30  # em px
        self.cor_pincel = "black"  # white ou black apenas
        self.isInBorracha = False

    def set_quadro_desenho_binds(self):
        # print("Iniciando quadro de edicao")
        self.quadro_desenho.set_cursor('pencil')
        # Botando as binds no quadro_desenho apenas, antes tava para toda a janela por isso tava bugando
        self.quadro_desenho.Widget.bind('<Button-1>', self.save_pos)
        self.quadro_desenho.Widget.bind("<B1-Motion>", self.pintar)

    def save_pos(self, event):
        self.lastx, self.lasty = event.x, event.y

    def pintar(self, event):
        # Aparentemente isso funciona, me impressionei comigo mesmo
        if self.isInBorracha == True:
            figuras = self.quadro_desenho.get_figures_at_location(location=(event.x, 300 - event.y))
            #N precisa desse if, já que de qualquer jeito a gente vai precisar tirar o primeiro elemento dessa tupla
            #if figuras != (1,):
            figuras = figuras[1:]  # Remove o primeiro elemento das figuras, que é a imagem de fundo(n sei pq é assim, mas é)
            for figura in figuras:
                self.quadro_desenho.delete_figure(figura)

        else:
            self.quadro_desenho.draw_rectangle((self.lastx, 300 - self.lasty), (event.x, 300 - event.y),
                                               line_color=self.cor_pincel, line_width=self.tamanho_pincel)

        self.save_pos(event)

    # OBS: gambiarra fudida
    def limpar(self):
        self.quadro_desenho.Widget.delete("all")  # Apaga tudo, deixando um quadro em branco
        self.quadro_desenho.draw_image(filename=DIRETORIO_TRANS_ORIGINAL, location=(0, 300))  # Bota imagem de novo

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
        if self.isInBorracha == True:
            self.isInBorracha = False
            self.quadro_desenho.set_cursor('pencil')
            self.telaprincipal['corbtn'].update(
                button_color=('white' if self.cor_pincel == 'black' else 'black', self.cor_pincel))
        elif self.cor_pincel == 'white':
            self.cor_pincel = "black"
            self.telaprincipal['corbtn'].update(button_color=('white', self.cor_pincel))
            self.telaprincipal['freqslider'].update(range=(0, 0.9), value=self.multiplicadorFreq[0])
        else:
            self.cor_pincel = 'white'
            self.telaprincipal['corbtn'].update(button_color=('black', self.cor_pincel))
            self.telaprincipal['freqslider'].update(range=(1, 5), value=self.multiplicadorFreq[1])

    def open_result(self, image):
        layout_column2 = [
            [sg.Text("Resultado da Sua Edição", size=(80, 1), justification="center")],
            [sg.Button(image_filename=image, image_size=(300, 300), key="userimg")],
            [sg.Button("Voltar a editar", key="anterior")]
        ]

        layout = [[sg.Column(layout_column2, element_justification='center')]]

        window = sg.Window("IFFT", layout, size=(LARGURA_JANELA, ALTURA_JANELA))

        # Interagindo o a segunda janela
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "anterior":
                window.close()

        window.close()

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
                case "salvarbtn":
                    self.salvar()
                    filtro = cria_filtro_do_desenho(self.multiplicadorFreq)
                    resultado(filtro, self.transformada)
                    imgresult = "../data/trans&result/resultado.png"
                    self.open_result(imgresult)
                case "limpabtn":
                    self.limpar()
                case "aumentabtn":
                    self.aumentar_pincel()
                    self.telaprincipal["tamtxt"].update(f'{self.tamanho_pincel} px')
                case "diminuibtn":
                    self.diminuir_pincel()
                    self.telaprincipal["tamtxt"].update(f'{self.tamanho_pincel} px')
                case 'freqslider':

                    if self.cor_pincel == 'black':
                        self.multiplicadorFreq[0] = self.values['freqslider']
                        txt = "Diminuindo frequencias"

                    else:
                        self.multiplicadorFreq[1] = self.values['freqslider']
                        txt = "Amplificando frequencias"
                    self.telaprincipal["textslider"].update(f"{txt}")
                    self.telaprincipal["valoresPreto"].update(f"Preto: {self.multiplicadorFreq[0]}")
                    self.telaprincipal["valoresBranco"].update(f"Branco: {self.multiplicadorFreq[1]}")

                case 'borrachabtn':
                    self.isInBorracha = True
                    self.quadro_desenho.set_cursor('plus')
                    self.telaprincipal["corbtn"].update(button_color="#808080")
        self.telaprincipal.close()


# Pode apagar depois após a criação da tela seguinte
def resultado(filtro, transformada):
    f_center_filtrado = filtro * transformada

    img = inversa_para_imagem(transformada_inversa(f_center_filtrado))

    cv2.imwrite("../data/trans&result/resultado.png", img)
