# -*- encoding: utf-8 -*-
import pilas
from pilas.actores.globo import Globo


class GloboElegir(Globo):
    """Representa un mensaje de globo (similar a las historietas), pero con opciones para elegir.

        >>> mensaje = u"Mi color favorito es el..."
        >>> globo = pilas.actores.GloboElegir(mensaje, [u"rojo", u"verde", u"azul"], cuando_responde_color_favorito)

    .. image:: images/actores/globo_elegir.png

    El primer argumento es el mensaje a mostrar, el segundo una lista de opciones que se ofrecerán
    y por último una función de respuesta. Que podría ser codificada así:

    .. code-block:: python

        def cuando_responde_color_favorito(respuesta):
            print "Ha seleccionado la opcion: " + respuesta

    """

    def __init__(self, texto, opciones, funcion_a_invocar, x=0, y=0, dialogo=None):
        """Constructor del dialogo:

        :param texto: Cadena de texto que se tiene que mostrar.
        :param opciones: Lista de opciones a mostrar.
        :param funcion_a_invocar: Referencia a la función que se tiene que ejecutar cuando responde el usuario.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param dialogo: Instancia del manejador de dialogos, para crear mensajes enlazados.
        """
        self.dialogo = dialogo
        self.opciones = opciones
        self.funcion_a_invocar = funcion_a_invocar

        self.lista_seleccion = pilas.interfaz.ListaSeleccion(opciones, self._cuando_selecciona_opcion, x, y)
        self.lista_seleccion.escala = 0.1
        self.lista_seleccion.escala = [1], 0.2
        self.lista_seleccion.z = 1

        Globo.__init__(self, texto, x, y, dialogo=dialogo,
                       ancho_globo=self.lista_seleccion.ancho_opciones+24,
                       alto_globo=self.lista_seleccion.alto_opciones + (self.lista_seleccion.separacion_entre_opciones * len(self.opciones) * 2))
        self.z = 2

    def colocar_origen_del_globo(self, x, y):
        """Cambia el punto de referencia del globo.

        :param x: Punto de referencia horizontal.
        :param y: Punto de referencia vertical.
        """
        Globo.colocar_origen_del_globo(self, x, y)

        self.lista_seleccion.centro = ("derecha", "abajo")
        self.lista_seleccion.x = x - (self.ancho_globo - self.lista_seleccion.ancho_opciones) + 12
        self.lista_seleccion.y = y + 35

    def _obtener_area_para_el_texto(self, texto):
        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)
        opciones_ancho, opciones_alto = self.lienzo.obtener_area_para_lista_de_texto(self.opciones, tamano=14)
        return ancho + opciones_ancho, alto + opciones_alto

    def _escribir_texto(self, texto):
        self.lienzo.escribir(texto, 12, 25, tamano=14)

    def cuando_quieren_avanzar(self, *k):
        pass

    def _cuando_selecciona_opcion(self, opcion):
        self.funcion_a_invocar(opcion)
        Globo.cuando_quieren_avanzar(self)
        self.lista_seleccion.eliminar()
