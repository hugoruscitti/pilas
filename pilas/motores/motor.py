# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


def abstract():
    raise Exception("Tienes que re-definir este metodo.")

class Motor(object):
    
    def __init__(self):
        pass

    def obtener_actor(self, imagen, x, y):
        abstract()

    def obtener_texto(self, texto, x, y):
        abstract()
    
    def obtener_canvas(self, ancho, alto):
        abstract()
    
    def obtener_grilla(self, ruta, columnas, filas):
        abstract()

    def crear_ventana(self, ancho, alto, titulo):
        abstract()

    def ocultar_puntero_del_mouse(self):
        abstract()

    def mostrar_puntero_del_mouse(self):
        abstract()

    def cerrar_ventana(self):
        abstract()

    def dibujar_circulo(self, x, y, radio, color, color_borde):
        abstract()

    def pulsa_tecla(self, tecla):
        abstract()

    def centrar_ventana(self):
        abstract()

    def procesar_y_emitir_eventos(self):
        abstract()

    def procesar_evento_teclado(self, event):
        abstract()

    def definir_centro_de_la_camara(self, x, y):
        abstract()

    def obtener_centro_de_la_camara(self):
        abstract()

    def pintar(self, color):
        abstract()

    def cargar_sonido(self, ruta):
        abstract()

    def cargar_imagen(self, ruta):
        abstract()

    def obtener_imagen_cairo(self, imagen):
        abstract()
