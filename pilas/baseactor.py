# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas.utils

class Estudiante:
    """Representa la habilidad de poder realizar habiliadades y comportamientos."""

    def __init__(self):
        self.habilidades = []
        self.comportamiento_actual = None
        self.comportamientos = []
        self.repetir_comportamientos_por_siempre = False

    def aprender(self, classname, *k, **w):
        "Comienza a realizar una habilidad indicada por parametros."
        objeto_habilidad = classname(self, *k, **w)
        self.habilidades.append(objeto_habilidad)

    def hacer_luego(self, comportamiento, repetir_por_siempre=False):
        """Define un nuevo comportamiento para realizar al final.
        
        Los actores pueden tener una cadena de comportamientos, este
        metodo agrega el comportamiento al final de la cadena.
        """
        
        self.comportamientos.append(comportamiento)
        self.repetir_comportamientos_por_siempre = repetir_por_siempre

    def hacer(self, comportamiento):
        "Define el comportamiento para el actor de manera inmediata."
        self.comportamientos.append(comportamiento)
        self._adoptar_el_siguiente_comportamiento()

    def eliminar_habilidades(self):
        "Elimina todas las habilidades asociadas al actor."
        for h in self.habilidades:
            h.eliminar()

    def eliminar_comportamientos(self):
        "Elimina todos los comportamientos que tiene que hacer el actor."
        for c in self.comportamientos:
            c.eliminar()

    def actualizar_habilidades(self):
        for h in self.habilidades:
            h.actualizar()

    def actualizar_comportamientos(self):
        termina = None

        if self.comportamiento_actual:
            termina = self.comportamiento_actual.actualizar()

            if termina:
                if self.repetir_comportamientos_por_siempre:
                    self.comportamientos.append(self.comportamiento_actual)
                self._adoptar_el_siguiente_comportamiento()
        else:
            self._adoptar_el_siguiente_comportamiento()

    def _adoptar_el_siguiente_comportamiento(self):
        if self.comportamientos:
            self.comportamiento_actual = self.comportamientos.pop(0)
            self.comportamiento_actual.iniciar(self)
        else:
            self.comportamiento_actual = None

class BaseActor(object, Estudiante):
    """Define la funciondad abstracta de un actor.

    La responsabilidad de esta clase es:

        - Controlar la posicion y el area que ocupa en pantalla.

    La clase que extienda a este debe tener
    métodos para dar el tamano del sprite, informar y alterar
    la posicion en pantalla.
    """

    def __init__(self, x=0, y=0):
        self._definir_centro_del_actor()
        Estudiante.__init__(self)

        self.x = x
        self.y = y

        # Define el nivel de lejania respecto del observador.
        self.z = 0
        self._espejado = False
        self.radio_de_colision = 10
        pilas.actores.utils.insertar_como_nuevo_actor(self)
        self._transparencia = 0

    def _definir_centro_del_actor(self):
        "Hace que el eje de posición del actor sea el centro de la imagen."
        size = self.obtener_area()
        self.definir_centro(size[0]/2, size[1]/2)

    def get_x(self):
        x, y = self.obtener_posicion()
        return x

    @pilas.utils.interpolable
    def set_x(self, x):
        self.definir_posicion(x, self.y)

    def get_z(self):
        return self._z

    @pilas.utils.interpolable
    def set_z(self, z):
        self._z = z
        pilas.actores.utils.ordenar_actores_por_valor_z()

    @pilas.utils.interpolable
    def set_y(self, y):
        self.definir_posicion(self.x, y)

    def get_y(self):
        x, y = self.obtener_posicion()
        return y

    @pilas.utils.interpolable
    def set_scale(self, s):
        if s <= 0:
            return

        ultima_escala = self.obtener_escala()

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

    @pilas.utils.interpolable
    def set_rotation(self, x):
        self.definir_rotacion(x)

    def get_espejado(self):
        return self._espejado

    def set_espejado(self, nuevo_valor):
        if self._espejado != nuevo_valor:
            self._espejado = nuevo_valor
            self.FlipX(self._espejado)

    @pilas.utils.interpolable
    def set_transparencia(self, nuevo_valor):
        self._transparencia = nuevo_valor
        self.definir_transparencia(nuevo_valor)

    def get_transparencia(self):
        return self._transparencia

    def get_imagen(self):
        return self.obtener_imagen()

    def set_imagen(self, imagen):
        if isinstance(imagen, str):
            imagen = pilas.imagenes.cargar(imagen)

        self.definir_imagen(imagen)
        

    espejado = property(get_espejado, set_espejado, doc="Indica si se tiene que invertir horizonaltamente la imagen del actor.")
    z = property(get_z, set_z, doc="Define lejania respecto del observador.")
    x = property(get_x, set_x, doc="Define la posición horizontal.")
    y = property(get_y, set_y, doc="Define la posición vertical.")
    rotacion = property(get_rotation, set_rotation, doc="Angulo de rotación (en grados, de 0 a 360)")
    escala = property(get_scale, set_scale, doc="Escala de tamaño, 1 es normal, 2 al doble de tamaño etc...)")
    transparencia = property(get_transparencia, set_transparencia, doc="Define el nivel de transparencia, 0 indica opaco y 100 la maxima transparencia.")
    imagen = property(get_imagen, set_imagen, doc="Define la imagen a mostrar.")

    def eliminar(self):
        "Elimina el actor de la lista de actores que se imprimen en pantalla."
        pilas.actores.utils.eliminar_un_actor(self)
        self.eliminar_habilidades()
        self.eliminar_comportamientos()

    def actualizar(self):
        """Actualiza el estado del actor. 
        
        Este metodo se llama una vez por frame, y generalmente se redefine
        en alguna subclase."""
        pass

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


    def get_izquierda(self):
        return self.x - self.obtener_ancho()/2

    @pilas.utils.interpolable
    def set_izquierda(self, x):
        self.x = x + self.obtener_ancho()/2

    izquierda = property(get_izquierda, set_izquierda)

    def get_abajo(self):
        return self.y - self.obtener_alto()/2

    @pilas.utils.interpolable
    def set_abajo(self, y):
        self.y = y + self.obtener_alto()/2

    abajo = property(get_abajo, set_abajo)

    def get_derecha(self):
        return self.x + self.obtener_ancho()/2

    @pilas.utils.interpolable
    def set_derecha(self, x):
        self.x = x - self.obtener_ancho()/2

    derecha = property(get_derecha, set_derecha)

    def get_arriba(self):
        return self.y + self.obtener_alto()/2

    @pilas.utils.interpolable
    def set_arriba(self, y):
        self.y = y - self.obtener_alto()/2

    arriba = property(get_arriba, set_arriba)

    def colisiona_con_un_punto(self, x, y):
        "Determina si un punto colisiona con el area del actor."

        w, h = self.obtener_ancho(), self.obtener_alto()
        left, right = self.x - w/2 , self.x + w/2
        top, bottom = self.y - h/2,  self.y + h/2
        return left < x < right and top < y < bottom
