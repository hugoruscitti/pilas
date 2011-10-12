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

    def iniciar_ventana(self, ancho, alto, titulo, pantalla_completa):
        abstract()

    def mostrar_ventana(self, pantalla_completa):
        abstract()

    def pantalla_completa(self):
        abstract()

    def pantalla_modo_ventana(self):
        abstract()

    def esta_en_pantalla_completa(self):
        abstract()

    def alternar_pantalla_completa(self):
        abstract()

    def centro_fisico(self):
        abstract()

    def obtener_area(self):
        abstract()

    def centrar_ventana(self):
        abstract()

    def obtener_actor(self, imagen, x, y):
        abstract()

    def obtener_texto(self, texto, magnitud):
        abstract()

    def obtener_grilla(self, ruta, columnas, filas):
        abstract()

    def actualizar_pantalla(self):
        abstract()

    def definir_centro_de_la_camara(self, x, y):
        abstract()

    def obtener_centro_de_la_camara(self):
        abstract()

    def cargar_sonido(self, ruta):
        abstract()

    def cargar_imagen(self, ruta):
        abstract()

    def obtener_lienzo(self):
        abstract()

    def obtener_superficie(self, ancho, alto):
        abstract()

    def ejecutar_bucle_principal(self, mundo, ignorar_errores):
        abstract()

    def realizar_actualizacion_logica(self):
        abstract()

    def obtener_codigo_de_tecla_normalizado(self, tecla_qt):
        abstract()

    def escala(self):
        abstract()

    def obtener_area_de_texto(self, texto, magnitud=10):
        abstract()

    def alternar_pausa(self):
        abstract()

    def ocultar_puntero_del_mouse(self):
        abstract()

    def terminar(self):
        abstract()
