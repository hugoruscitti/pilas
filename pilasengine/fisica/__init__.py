# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.fisica.contact_listener import ObjetosContactListener
from pilasengine.fisica import rectangulo
from pilasengine.fisica import circulo
from pilasengine.fisica.constantes import constante_de_movimiento
import figura

PPM = 30

import math
import random

try:
    import Box2D as box2d
    contact_listener = box2d.b2ContactListener
except ImportError:
    class Tmp:
        pass
    contact_listener = Tmp


class Fisica(object):
    """Representa un simulador de mundo fisico, usando la biblioteca Box2D (version 2.1)."""

    def __init__(self, escena, pilas):
        """Inicializa el motor de física.

        :param area: El area del escenario, en forma de tupla.
        :param gravedad: La aceleración del escenario.
        """
        gravedad = (0, -10)

        self.pilas = pilas
        self.escena = escena
        self.mundo = None
        self.mundo = box2d.b2World(gravedad, True)
        self.objetosContactListener = ObjetosContactListener(pilas)
        self.mundo.contactListener = self.objetosContactListener
        self.figuras_a_eliminar = []
        self.constante_mouse = None

        self.velocidad = 1.0
        self.timeStep = self.velocidad/60.0
        self.optimizar_figuras_estaticas(False)

    def optimizar_figuras_estaticas(self, estado=True):
        """Le indica al motor de fisica que no calcule colisiones en figuras que están en reposo."""
        self.mundo.SetAllowSleeping(estado)
        self.mundo.continuousPhysics = (not estado)

    def iniciar(self):
        self.area = self.pilas.obtener_widget().obtener_area()
        self.crear_bordes_del_escenario()

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

        self.constante_mouse = constante_de_movimiento.ConstanteDeMovimiento(self.pilas, figura)

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

    def actualizar(self):
        """Realiza la actualización lógica del escenario.
        """
        if self.mundo:
            self.mundo.Step(self.timeStep, 6, 3)
            self._procesar_figuras_a_eliminar()
            self.mundo.ClearForces()

    def iterar(self):
        self.actualizar()

    def pausar_mundo(self):
        """Detiene la simulación física."""
        if self.mundo:
            self.timeStep = 0

    def reanudar_mundo(self):
        """Restaura la simulación física."""

        if self.mundo:
            self.timeStep = self.velocidad/60.0

    def _procesar_figuras_a_eliminar(self):
        "Elimina las figuras que han sido marcadas para quitar."
        if self.figuras_a_eliminar:
            for x in self.figuras_a_eliminar:
                # Solo elimina las figuras que actualmente existen.
                if x in self.mundo.bodies:
                    self.mundo.DestroyBody(x)
            self.figuras_a_eliminar = []

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
        self.suelo = self.Rectangulo(0, -alto/2, ancho, 2, dinamica=False, plataforma=True, restitucion=restitucion)

    def crear_techo(self, (ancho, alto), restitucion=0):
        """Genera un techo sólido para el escenario.

        :param ancho: El ancho del techo.
        :param alto: Alto del techo.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.techo = self.Rectangulo(0, alto/2, ancho, 2, dinamica=False, plataforma=True, restitucion=restitucion)

    def crear_paredes(self, (ancho, alto), restitucion=0):
        """Genera dos paredes para el escenario.

        :param ancho: El ancho de las paredes.
        :param alto: El alto de las paredes.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.pared_izquierda = self.Rectangulo(-ancho/2, 0, 2, alto, dinamica=False, plataforma=True, restitucion=restitucion)
        self.pared_derecha = self.Rectangulo(ancho/2, 0, 2, alto, dinamica=False, plataforma=True, restitucion=restitucion)

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

    def despertar_a_todos(self):
        for x in self.mundo.bodies:
            x.awake = True

    def definir_gravedad(self, x, y):
        """Define la gravedad del motor de física.

        :param x: Aceleración horizontal.
        :param y: Aceleración vertical.
        """
        self.mundo.gravity = (x, y)
        self.despertar_a_todos()

    def obtener_gravedad_x(self):
        (x, _) = self.mundo.gravity
        return x

    def definir_gravedad_x(self, x):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'set_gravedad_x', x)

    def obtener_gravedad_y(self):
        (_, y) = self.mundo.gravity
        return y

    def definir_gravedad_y(self, y):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'set_gravedad_y', y)

    gravedad_x = property(obtener_gravedad_x, definir_gravedad_x)
    gravedad_y = property(obtener_gravedad_y, definir_gravedad_y)

    def set_gravedad_x(self, nuevo_x):
        (_, y) = self.mundo.gravity
        self.mundo.gravity = (nuevo_x, y)
        self.despertar_a_todos()

    def set_gravedad_y(self, nuevo_y):
        (x, _) = self.mundo.gravity
        self.mundo.gravity = (x, nuevo_y)
        self.despertar_a_todos()

    _set_gravedad_x = property(obtener_gravedad_x, set_gravedad_x)
    _set_gravedad_y = property(obtener_gravedad_y, set_gravedad_y)

    def eliminar_para_liberar_memoria(self):
        lista = list(self.mundo.bodies)

        for cuerpo in lista:
            for fixture in cuerpo:
                cuerpo.DestroyFixture(fixture)

            self.mundo.DestroyBody(cuerpo)

        import gc
        gc.collect()

    def Rectangulo(self, x=0, y=0, ancho=50, alto=20, dinamica=True, densidad=1.0,
                   restitucion=0.56, friccion=10.5, amortiguacion=0.1,
                   sin_rotacion=False, sensor=False, plataforma=False):
        ":rtype: rectangulo.Rectangulo"

        return rectangulo.Rectangulo(self, self.pilas, x, y, ancho, alto,
                                    dinamica=dinamica, densidad=densidad,
                                    restitucion=restitucion, friccion=friccion,
                                    amortiguacion=amortiguacion,
                                    sin_rotacion=sin_rotacion,
                                    sensor=sensor,
                                    plataforma=plataforma)

    def Circulo(self, x=0, y=0, radio=20, dinamica=True, densidad=1.0,
                restitucion=0.56, friccion=10.5, amortiguacion=0.1,
                sin_rotacion=False, sensor=False):
        return circulo.Circulo(self, self.pilas, x, y, radio,
                               dinamica=dinamica, densidad=densidad,
                               restitucion=restitucion, friccion=friccion,
                               amortiguacion=amortiguacion, sin_rotacion=sin_rotacion,
                               sensor=sensor)
