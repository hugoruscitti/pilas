# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

from PySFML import sf
import math

todos = []

RADIO_INICIAL = 10

def ordenar_actores_por_valor_z():
    "Ordena todos los actores para que se impriman con 'z' como criterio de orden."
    todos.sort()

def insertar_como_nuevo_actor(actor):
    "Coloca a un actor en la lista de actores a imprimir en pantalla."
    todos.append(actor)
    
def eliminar_un_actor(actor):
    todos.remove(actor)

def eliminar_a_todos():
    a_eliminar = list(todos)

    for x in a_eliminar:
        x.eliminar()

def obtener_actor_en(x, y):
    "Intenta obtener el actor mas cerca de la pantalla (z mas pequeño) en la posición (x, y)"

    # Busca el objeto que colisiones ordenando en sentido inverso.
    for sprite in todos[::-1]:
        if sprite.colisiona_con_un_punto(x, y):
            return sprite

    return None



class Estudiante:
    "Permite a distintos objetos acoplarse mediente mixins."

    def aprender(self, classname, *k, **w):
        if not classname in self.__class__.__bases__:
            self.__class__.__bases__ += (classname,)
        classname.__init__(self, *k, **w)


class BaseActor(object, Estudiante):
    "Define la funcionalidad abstracta de un actor."

    def __init__(self):
        insertar_como_nuevo_actor(self)
        self._set_central_axis()
        self.comportamiento = None

        # define la posicion inicial.
        self.SetPosition(0, 0)

        # Define el nivel de lejania respecto del observador.
        self.z = 0
        self._espejado = False
        self.radio_de_colision = RADIO_INICIAL

    def _set_central_axis(self):
        "Hace que el eje de posición del actor sea el centro de la imagen."
        size = self.GetSize()
        self.SetCenter(size[0]/2, size[1]/2)

    def get_x(self):
        x, y = self.GetPosition()
        return x

    def set_x(self, x):
        if pilas.utils.es_interpolacion(x):
            x.apply(self, function='set_x')
        else:
            self.SetX(x)

    def get_z(self):
        return self._z

    def set_z(self, z):
        if pilas.utils.es_interpolacion(z):
            print "Lo siento, sobre z no puede aplicar una interpolacion..."
        else:
            self._z = z

        ordenar_actores_por_valor_z()

    def set_y(self, y):
        if pilas.utils.es_interpolacion(y):
            y.apply(self, function='set_y')
        else:
            self.SetY(-y)

    def get_y(self):
        x, y = self.GetPosition()
        return -y

    def set_scale(self, s):
        if pilas.utils.es_interpolacion(s):
            s.apply(self, function='set_scale')
        else:
            if s <= 0:
                return

            (ultima_escala, _) = self.GetScale()

            # Se hace la siguiente regla de 3 simple:
            #
            #  ultima_escala          self.radio_de_colision
            #  s                      ?

            self.SetScale(s, s)
            self.radio_de_colision = (s * self.radio_de_colision) / ultima_escala

    def get_scale(self):
        # se asume que la escala del personaje es la horizontal.
        return self.GetScale()[0]

    def get_rotation(self):
        return self.GetRotation()

    def set_rotation(self, x):

        if pilas.utils.es_interpolacion(x):
            x.apply(self, function='set_rotation')
        else:
            self.SetRotation(x)

    def get_espejado(self):
        return self._espejado

    def set_espejado(self, nuevo_valor):
        if self._espejado != nuevo_valor:
            self._espejado = nuevo_valor
            self.FlipX(self._espejado)

    espejado = property(get_espejado, set_espejado, doc="Indica si se tiene que invertir horizonaltamente la imagen del actor.")
    z = property(get_z, set_z, doc="Define lejania respecto del observador.")
    x = property(get_x, set_x, doc="Define la posición horizontal.")
    y = property(get_y, set_y, doc="Define la posición vertical.")
    rotacion = property(get_rotation, set_rotation, doc="Angulo de rotación (en grados, de 0 a 360)")
    escala = property(get_scale, set_scale, doc="Escala de tamaño, 1 es normal, 2 al doble de tamaño etc...)")


    def eliminar(self):
        "Elimina el actor de la lista de actores que se imprimen en pantalla."
        eliminar_un_actor(self)


    def actualizar(self):
        "Actualiza el estado del actor. Este metodo se llama una vez por frame."

        if self.comportamiento:
            termina = self.comportamiento.actualizar()

            if termina:
                self.comportamiento.terminar()
                self.comportamiento = None

    def __cmp__(self, otro_actor):
        """Compara dos actores para determinar cual esta mas cerca de la camara.

        Este metodo se utiliza para ordenar los actores antes de imprimirlos
        en pantalla. De modo tal que un usuario pueda seleccionar que
        actores se ven mas arriba de otros cambiando los valores de
        los atributos `z`."""

        if otro_actor.z >= self.z:
            return 1
        else:
            return -1

    def hacer(self, comportamiento):
        "Define un nuevo comportamiento para el actor."

        comportamiento.iniciar(self)
        self.comportamiento = comportamiento

    def get_izquierda(self):
        return self.x - self.obtener_ancho()/2

    def set_izquierda(self, x):
        self.x = x + self.obtener_ancho()/2

    izquierda = property(get_izquierda, set_izquierda)

    def get_abajo(self):
        return self.y - self.obtener_alto()/2

    def set_abajo(self, y):
        self.y = y + self.obtener_alto()/2

    abajo = property(get_abajo, set_abajo)

    def get_derecha(self):
        return self.x + self.obtener_ancho()/2

    def set_derecha(self, x):
        self.x = x - self.obtener_ancho()/2

    derecha = property(get_derecha, set_derecha)

    def get_arriba(self):
        return self.y + self.obtener_alto()/2

    def set_arriba(self, y):
        self.y = y - self.obtener_alto()/2

    arriba = property(get_arriba, set_arriba)

class Actor(sf.Sprite, BaseActor):
    """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

    Un objeto Actor se tiene que crear siempre indicando la imagen, ya
    sea como una ruta a un archivo como con un objeto Image. Por ejemplo::

        protagonista = Actor("protagonista_de_frente.png")

    es equivalente a:

        imagen = pilas.imagenes.cargar("protagonista_de_frente.png")
        protagonista = Actor(imagen)

    Luego, na vez que ha sido ejecutada la sentencia aparecerá en el centro de
    la pantalla el nuevo actor para que pueda manipularlo. Por ejemplo
    alterando sus propiedades::

        protagonista.x = 100
        protagonista.scale = 2
        protagonista.rotation = 30


    Estas propiedades tambien se pueden manipular mediante
    interpolaciones. Por ejemplo, para aumentar el tamaño del
    personaje de 1 a 5 en 7 segundos::

        protagonista.scale = pilas.interpolar(1, 5, 7)

    Si creas un sprite sin indicar la imagen se cargará
    una por defecto.
    """

    def __init__(self, image="sin_imagen.png"):

        if isinstance(image, str):
            image = pilas.imagenes.cargar(image)

        sf.Sprite.__init__(self, image)
        BaseActor.__init__(self)


    def colisiona_con_un_punto(self, x, y):
        "Determina si un punto colisiona con el area del actor."
        w, h = self.GetSize()
        left, right = self.x - w/2 , self.x + w/2
        top, bottom = self.y - h/2,  self.y + h/2
        return left < x < right and top < y < bottom

    def dibujar(self, aplicacion):
        aplicacion.Draw(self)

    def duplicar(self, **kv):
        duplicado = self.__class__()

        for clave in kv:
            setattr(duplicado, clave, kv[clave])

        return duplicado

    def obtener_ancho(self):
        return self.GetSize()[0]

    def obtener_alto(self):
        return self.GetSize()[1]

    def __str__(self):
        return "<%s en (%d, %d)>" %(self.__class__.__name__, self.x, self.y)

from mono import *
from tortuga import *
from texto import *
from ejes import *
from pingu import Pingu
from pizarra import Pizarra
from animado import Animado
from animacion import Animacion
from explosion import Explosion
from banana import Banana
from bomba import Bomba
from moneda import Moneda
