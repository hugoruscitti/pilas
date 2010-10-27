# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas.utils

class Estudiante:
    "Permite a distintos objetos acoplarse mediente mixins."

    def aprender(self, classname, *k, **w):
        if not classname in self.__class__.__bases__:
            self.__class__.__bases__ += (classname,)
        classname.__init__(self, *k, **w)

        print "Aprendiendo habibilidad", classname


class BaseActor(object, Estudiante):
    """Define la funciondad abstracta de un actor.

    La responsabilidad de esta clase es:

        - Controlar la posicion y el area que ocupa en pantalla.

    La clase que extienda a este debe tener
    métodos para dar el tamano del sprite, informar y alterar
    la posicion en pantalla.
    """

    def __init__(self):
        self._definir_centro_del_actor()
        self.comportamiento = None

        self.x = 0
        self.y = 0

        # Define el nivel de lejania respecto del observador.
        self.z = 0
        self._espejado = False
        self.radio_de_colision = 10
        pilas.actores.utils.insertar_como_nuevo_actor(self)

    def _definir_centro_del_actor(self):
        "Hace que el eje de posición del actor sea el centro de la imagen."
        size = self.obtener_area()
        self.definir_centro(size[0]/2, size[1]/2)

    def get_x(self):
        x, y = self.obtener_posicion()
        return x

    def set_x(self, x):
        if pilas.utils.es_interpolacion(x):
            x.apply(self, function='set_x')
        else:
            self.definir_posicion(x, self.y)

    def get_z(self):
        return self._z

    def set_z(self, z):
        if pilas.utils.es_interpolacion(z):
            print "Lo siento, sobre z no puede aplicar una interpolacion..."
        else:
            self._z = z

        pilas.actores.utils.ordenar_actores_por_valor_z()

    def set_y(self, y):
        if pilas.utils.es_interpolacion(y):
            y.apply(self, function='set_y')
        else:
            self.definir_posicion(self.x, -y)

    def get_y(self):
        x, y = self.obtener_posicion()
        return -y

    def set_scale(self, s):
        if pilas.utils.es_interpolacion(s):
            s.apply(self, function='set_scale')
        else:
            if s <= 0:
                return

            (ultima_escala, _) = self.obtener_escala()

            # Se hace la siguiente regla de 3 simple:
            #
            #  ultima_escala          self.radio_de_colision
            #  s                      ?

            self.definir_escala(s)
            self.radio_de_colision = (s * self.radio_de_colision) / ultima_escala

    def get_scale(self):
        return self.obtener_escala()

    def get_rotation(self):
        return self.obtener_rotacion()

    def set_rotation(self, x):

        if pilas.utils.es_interpolacion(x):
            x.apply(self, function='set_rotation')
        else:
            self.definir_rotacion(x)

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
        #eliminar_un_actor(self)
        print "TODO, esta funcion se borro"

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

    def colisiona_con_un_punto(self, x, y):
        "Determina si un punto colisiona con el area del actor."
        w, h = self.obtener_ancho(), self.obtener_alto()
        left, right = self.x - w/2 , self.x + w/2
        top, bottom = self.y - h/2,  self.y + h/2
        return left < x < right and top < y < bottom
