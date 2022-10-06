from PIL import Image, ImageGrab
from io import BytesIO
#Usem esse arquivo para salvar valores que vocês repetem muito, tipo variaveis, fotos, etc

LARGURA_JANELA, ALTURA_JANELA = 450, 600


#Funções suporte
def array_to_data(array):
    im = Image.fromarray(array)
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

def save_element_as_file(element, filename):
    widget = element.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    grab.save(filename)
