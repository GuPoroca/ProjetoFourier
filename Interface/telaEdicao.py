import PIL  # Pra add essa dependencia, precisa usar o pip install pillow
import PySimpleGUI as sg

# TODO >_<
#   Principal: adicionar imagem para ser editada
#   Adicionar botões de mudar de cor(preto, branco), aumentar/diminuir pincel, limpar tela, e avançar

LARGURA_JANELA, ALTURA_JANELA = 450, 600

IMAGEM = "../data/monke.png"


class TelaEdicao:
    # Construtor, java é melhor
    def __init__(self):
        self.lastx = None
        self.lasty = None

        self.layout = [[sg.Canvas(background_color="#ffffff", size=(LARGURA_JANELA - 50, ALTURA_JANELA - 100),
                                  pad=(5, 5), key="quadro_desenho",
                                  tooltip="Edite aqui", visible=True, border_width=10)], [sg.Text("Botoes quadro")],
                       [sg.Button('Mostrar posicao mouse', button_color=("#000000", "#991a1a")),
                        sg.Exit("Sair", button_color=("#000000", "#991a1a"))]]

        self.telaprincipal = sg.Window("Photoshopee", self.layout, size=(LARGURA_JANELA, ALTURA_JANELA), finalize=True)
        self.quadro_desenho = self.telaprincipal["quadro_desenho"]  # self.telaprincipal.Element("quadro_desenho")
        self.key = None
        self.values = None
        self.event = 'Exit'

    def iniciarQuadroEdicao(self):
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
        self.quadro_desenho.Widget.create_line((self.lastx, self.lasty, event.x, event.y), fill='#000000')
        self.save_pos(event)
        print(event.x, event.y)
        print(self.lastx, self.lasty)

    def limpar(self) -> None:
        self.quadro_desenho.delete("all")


    def run(self) -> None:
        self.iniciarQuadroEdicao()
        while True:  # A brincadeira eh aq
            self.event, self.values = self.telaprincipal.read()

            if self.event == sg.WIN_CLOSED or self.event == 'Sair':
                break

        self.telaprincipal.close()


TelaEdicao().run()
