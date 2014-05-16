# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.fisica.contact_listener import ObjectContactListener

PPM = 30

import math
import random

try:
    import Box2D as box2d
    contact_listener = box2d.b2ContactListener
    __enabled__ = True
except ImportError:
    __enabled__ = False
    class Tmp:
        pass
    contact_listener = Tmp


def convertir_a_metros(valor):
    """Convierte una magnitid de pixels a metros."""
    return valor / float(PPM)

def convertir_a_pixels(valor):
    """Convierte una magnitud de metros a pixels."""
    return valor * PPM


class Fisica(object):
    """Representa un simulador de mundo fisico, usando la biblioteca Box2D (version 2.1)."""

    def __init__(self, escena):
        """Inicializa el motor de física.

        :param area: El area del escenario, en forma de tupla.
        :param gravedad: La aceleración del escenario.
        """
        gravedad = (0, -10)

        self.escena = escena
        self.pilas = escena.pilas
        self.mundo = box2d.b2World(gravedad, False)
        self.objetosContactListener = ObjetosContactListener()
        self.mundo.contactListener = self.objetosContactListener
        self.mundo.continuousPhysics = False

        self.area = self.pilas.obtener_area()
        self.figuras_a_eliminar = []

        self.constante_mouse = None
        self.crear_bordes_del_escenario()

        self.velocidad = 1.0
        self.timeStep = self.velocidad/120.0

    def crear_bordes_del_escenario(self):
        """Genera las paredes, el techo y el suelo."""
        self.crear_techo(self.area)
        self.crear_suelo(self.area)
        self.crear_paredes(self.area)

    def reiniciar(self):
        """Elimina todos los objetos físicos y vuelve a crear el entorno."""
        lista = list(self.mundo.bodies)

        for x in lista:
            self.mundo.DestroyBody(x)

        self.crear_bordes_del_escenario()

    def cantidad_de_cuerpos(self):
        return len(self.mundo.bodies)

    def capturar_figura_con_el_mouse(self, figura):
        """Comienza a capturar una figura con el mouse.

        :param figura: La figura a controlar con el mouse.
        """
        if self.constante_mouse:
            self.cuando_suelta_el_mouse()

        self.constante_mouse = ConstanteDeMovimiento(figura)

    def cuando_mueve_el_mouse(self, x, y):
        """Gestiona el evento de movimiento del mouse.

        :param x: Coordenada horizontal del mouse.
        :param y: Coordenada vertical del mouse.
        """
        if self.constante_mouse:
            self.constante_mouse.mover(x, y)

    def cuando_suelta_el_mouse(self):
        """Se ejecuta cuando se suelta el botón de mouse."""
        if self.constante_mouse:
            self.constante_mouse.eliminar()
            self.constante_mouse = None

    def actualizar(self, velocidad=1.0):
        """Realiza la actualización lógica del escenario.
        """
        # TODO: eliminar el arguemnto velocidad que no se utiliza.
        if self.mundo:
            self.mundo.Step(self.timeStep, 6, 3)
            self._procesar_figuras_a_eliminar()
            self.mundo.ClearForces()

    def pausar_mundo(self):
        """Detiene la simulación física."""
        if self.mundo:
            self.timeStep = 0

    def reanudar_mundo(self):
        """Restaura la simulación física."""
        if self.mundo:
            self.timeStep = self.velocidad/120.0

    def _procesar_figuras_a_eliminar(self):
        "Elimina las figuras que han sido marcadas para quitar."
        if self.figuras_a_eliminar:
            for x in self.figuras_a_eliminar:
                # Solo elimina las figuras que actualmente existen.
                if x in self.mundo.bodies:
                    self.mundo.DestroyBody(x)
            self.figuras_a_eliminar = []

    def dibujar_figuras_sobre_lienzo(self, motor, lienzo, grosor=1):
        """Dibuja todas las figuras en una pizarra. Indicado para depuracion.

        :param motor: Referencia al motor de pilas.
        :param lienzo: Un actor lienzo sobre el que se dibujará.
        :param grosor: El grosor de la linea medida en pixels.
        """

        cuerpos = self.mundo.bodies

        for cuerpo in cuerpos:

            for fixture in cuerpo:

                # cuerpo.type == 0 → estatico
                # cuerpo.type == 1 → kinematico
                # cuerpo.type == 2 → dinamico

                shape = fixture.shape

                if isinstance(shape, box2d.b2PolygonShape):
                    vertices = [cuerpo.transform * v * PPM for v in shape.vertices]
                    vertices = [pilas.escena_actual().camara.desplazar(v) for v in vertices]
                    lienzo.poligono(motor, vertices, color=pilas.colores.negro, grosor=grosor+2, cerrado=True)
                    lienzo.poligono(motor, vertices, color=pilas.colores.blanco, grosor=grosor, cerrado=True)
                elif isinstance(shape, box2d.b2CircleShape):
                    (x, y) = pilas.escena_actual().camara.desplazar(cuerpo.transform * shape.pos * PPM)

                    # Dibuja el angulo de la circunferencia.
                    lienzo.angulo(motor, x, y, - math.degrees(fixture.body.angle), shape.radius * PPM, pilas.colores.negro, grosor=grosor+2)
                    lienzo.angulo(motor, x, y, - math.degrees(fixture.body.angle), shape.radius * PPM, pilas.colores.blanco, grosor=grosor)

                    # Dibuja el borde de la circunferencia.
                    lienzo.circulo(motor, x, y, shape.radius * PPM, pilas.colores.negro, grosor=grosor+2)
                    lienzo.circulo(motor, x, y, shape.radius * PPM, pilas.colores.blanco, grosor=grosor)

                else:
                    # TODO: implementar las figuras de tipo "edge" y "loop".
                    raise Exception("No puedo identificar el tipo de figura.")


    def crear_cuerpo(self, definicion_de_cuerpo):
        """Genera un Body de box2d.

        :param definicion_de_cuerpo: Los parámetros de configuración de un cuerpo para Box2d.
        """
        return self.mundo.CreateBody(definicion_de_cuerpo)

    def crear_suelo(self, (ancho, alto), restitucion=0):
        """Genera un suelo sólido para el escenario.

        :param ancho: El ancho del suelo.
        :param alto: Alto del suelo.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.suelo = Rectangulo(0, -alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_techo(self, (ancho, alto), restitucion=0):
        """Genera un techo sólido para el escenario.

        :param ancho: El ancho del techo.
        :param alto: Alto del techo.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.techo = Rectangulo(0, alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_paredes(self, (ancho, alto), restitucion=0):
        """Genera dos paredes para el escenario.

        :param ancho: El ancho de las paredes.
        :param alto: El alto de las paredes.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.pared_izquierda = Rectangulo(-ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)
        self.pared_derecha = Rectangulo(ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)

    def eliminar_suelo(self):
        "Elimina el suelo del escenario."
        if self.suelo:
            self.suelo.eliminar()
            self.suelo = None

    def eliminar_techo(self):
        "Elimina el techo del escenario."
        if self.techo:
            self.techo.eliminar()
            self.techo = None

    def eliminar_paredes(self):
        "Elimina las dos paredes del escenario."
        if self.pared_izquierda:
            self.pared_derecha.eliminar()
            self.pared_izquierda.eliminar()
            self.pared_derecha = None
            self.pared_izquierda = None

    def eliminar_figura(self, figura):
        """Elimina una figura del escenario.

        :param figura: Figura a eliminar.
        """
        self.figuras_a_eliminar.append(figura)

    def obtener_distancia_al_suelo(self, x, y, dy):
        """Obtiene la distancia hacia abajo desde el punto (x,y).

        El valor de 'dy' tiene que ser positivo.

        Si la funcion no encuentra obstaculos retornara
        dy, pero en paso contrario retornara un valor menor
        a dy.

        :param x: posición horizontal del punto a analizar.
        :param y: posición vertical del punto a analizar.
        """

        if dy < 0:
            raise Exception("El valor de 'dy' debe ser positivo, ahora vale '%f'." %(dy))

        delta = 0

        while delta < dy:

            if self.obtener_cuerpos_en(x, y-delta):
                return delta

            delta += 1

        return delta

    def obtener_cuerpos_en(self, x, y):
        """Retorna una lista de cuerpos que se encuentran en la posicion (x, y) o retorna una lista vacia [].

        :param x: posición horizontal del punto a analizar.
        :param y: posición vertical del punto a analizar.
        """

        AABB = box2d.b2AABB()
        f = 1
        AABB.lowerBound = (x-f, y-f)
        AABB.upperBound = (x+f, y+f)

        cuantos, cuerpos = self.mundo.Query(AABB, 2)

        if cuantos == 0:
            return []

        lista_de_cuerpos = []

        for s in cuerpos:
            cuerpo = s.GetBody()

            if s.TestPoint(cuerpo.GetXForm(), (x, y)):
                lista_de_cuerpos.append(cuerpo)

        return lista_de_cuerpos

    def definir_gravedad(self, x, y):
        """Define la gravedad del motor de física.

        :param x: Aceleración horizontal.
        :param y: Aceleración vertical.
        """
        pilas.fisica.definir_gravedad(x, y)