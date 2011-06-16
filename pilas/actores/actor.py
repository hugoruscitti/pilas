# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.estudiante import Estudiante

IZQUIERDA = ["izquierda"]
DERECHA = ["derecha"]
ARRIBA = ["arriba", "superior"]
CENTRO = ["centro", "centrado", "medio", "arriba"]
ABAJO = ["abajo", "inferior", "debajo"]


class Actor(object, Estudiante):
    """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

    Un objeto Actor se tiene que crear siempre indicando la imagen, ya
    sea como una ruta a un archivo como con un objeto Image. Por ejemplo::

        protagonista = Actor("protagonista_de_frente.png")

    es equivalente a::

        imagen = pilas.imagenes.cargar("protagonista_de_frente.png")
        protagonista = Actor(imagen)

    Luego, na vez que ha sido ejecutada la sentencia aparecerá en el centro de
    la pantalla el nuevo actor para que pueda manipularlo. Por ejemplo
    alterando sus propiedades::

        protagonista.x = 100
        protagonista.escala = 2
        protagonista.rotacion = 30


    Estas propiedades tambien se pueden manipular mediante
    interpolaciones. Por ejemplo, para aumentar el tamaño del
    personaje de 1 a 5 en 7 segundos::

        protagonista.escala = 1
        protagonista.escala = [5], 7

    Si creas un actor sin indicarle la imagen, se cargará
    una imagen de una pila por defecto. Usa el nombre
    de imagen 'invisible.png' si no quieres motrar ninguna
    imagen.
    """

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):
        if not pilas.mundo:
            mensaje = "Tiene que invocar a la funcion ``pilas.iniciar()`` para comenzar."
            print mensaje
            raise Exception(mensaje)

        Estudiante.__init__(self)
        self._actor = pilas.mundo.motor.obtener_actor(imagen, x=x, y=y)
        self.centro = ('centro', 'centro')

        self.x = x
        self.y = y

        # Define el nivel de lejania respecto del observador.
        self.z = 0
        self._espejado = False
        self.radio_de_colision = 10
        pilas.actores.utils.insertar_como_nuevo_actor(self)
        self._transparencia = 0
        self.anexados = []

    def definir_centro(self, (x, y)):
        if type(x) == str:
            if x not in IZQUIERDA + CENTRO + DERECHA:
                raise Exception("No puedes definir '%s' como eje horizontal." %(x))
            x = self._interpretar_y_convertir_posicion(x, self.obtener_ancho())
        if type(y) == str:
            if y not in ARRIBA + CENTRO + ABAJO:
                raise Exception("No puedes definir '%s' como eje vertical." %(y))
            y = self._interpretar_y_convertir_posicion(y, self.obtener_alto())            

        self._centro = (x, y)
        self._actor.definir_centro(x, y)
    
    def _interpretar_y_convertir_posicion(self, posicion, maximo_valor):
        if posicion in IZQUIERDA + ARRIBA:
            return 0
        elif posicion in CENTRO:
            return int(maximo_valor / 2.0)
        elif posicion in DERECHA + ABAJO:
            return maximo_valor
        else:
            raise Exception("El valor '%s' no corresponde a una posicion, use numeros o valores como 'izquierda', 'arriba' etc." %(posicion))

    def obtener_centro(self):
        return self._centro
    
    centro = property(obtener_centro, definir_centro, "Define el punto de control del actor.")

    def definir_posicion(self, x, y):
        self._actor.definir_posicion(x, y)

    def obtener_posicion(self):
        return self._actor.obtener_posicion()

    def dibujar(self, aplicacion):
        self._actor.dibujar(aplicacion)

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
            self._actor.set_espejado(nuevo_valor)

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
        self.destruir()
        self._eliminar_anexados()
    
    def destruir(self):
        "Elimina a un actor pero de manera inmediata."
        pilas.actores.utils.eliminar_un_actor(self)
        self.eliminar_habilidades()
        self.eliminar_comportamientos()

    def actualizar(self):
        """Actualiza el estado del actor. 
        
        Este metodo se llama una vez por frame, y generalmente se redefine
        en alguna subclase."""
        self.actualizar_comportamientos()

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

############

    def get_izquierda(self):
        return self.x - (self.centro[0] * self.escala)

    @pilas.utils.interpolable
    def set_izquierda(self, x):
        self.x = x + (self.centro[0] * self.escala)

    izquierda = property(get_izquierda, set_izquierda)
    
    def get_derecha(self):
        return self.izquierda + self.obtener_ancho()

    @pilas.utils.interpolable
    def set_derecha(self, x):
        self.set_izquierda(x - self.ancho)

    derecha = property(get_derecha, set_derecha)


    def get_abajo(self):
        return self.get_arriba() - self.alto

    @pilas.utils.interpolable
    def set_abajo(self, y):
        self.set_arriba(y + self.alto)
        
    abajo = property(get_abajo, set_abajo)

    def get_arriba(self):
        return self.y + (self.centro[1] * self.escala)

    @pilas.utils.interpolable
    def set_arriba(self, y):
        self.y = y - (self.centro[1] * self.escala)

    arriba = property(get_arriba, set_arriba)

######

    def colisiona_con_un_punto(self, x, y):
        "Determina si un punto colisiona con el area del actor."
        return self.izquierda <= x <= self.derecha and self.abajo <= y <= self.arriba

    def obtener_rotacion(self):
        return self._actor.obtener_rotacion()

    def definir_rotacion(self, r):
        self._actor.definir_rotacion(r)

    def definir_color(self, c):
        self._actor.definir_color(c)

    def obtener_imagen(self):
        return self._actor.obtener_imagen()

    def definir_imagen(self, imagen):
        self._actor.definir_imagen(imagen)

    def duplicar(self, **kv):
        duplicado = self.__class__()

        for clave in kv:
            setattr(duplicado, clave, kv[clave])

        return duplicado

    def obtener_ancho(self):
        return self.imagen.ancho()

    def obtener_alto(self):
        return self.imagen.alto()

    ancho = property(obtener_ancho)
    alto = property(obtener_alto)

    def __mul__(self, cantidad):
        if type(cantidad) is not int or cantidad < 1:
            raise TypeError("Solo puede multiplicar por numeros enteros mayores a 1.")

        grupo = pilas.atajos.fabricar(self.__class__, cantidad - 1)
        grupo.append(self)
        return grupo

    def __str__(self):
        return "<%s en (%d, %d)>" %(self.__class__.__name__, self.x, self.y)

    def obtener_escala(self):
        return self._actor.obtener_escala()

    def definir_escala(self, escala):
        self._actor.definir_escala(escala)

    def definir_transparencia(self, valor):
        self._actor.definir_transparencia(valor)

    def imitar(self, otro_actor_o_figura):
        self.aprender(pilas.habilidades.Imitar, otro_actor_o_figura)

    def esta_fuera_de_la_pantalla(self):
        if self.derecha < -320 or self.izquierda > 320 or self.arriba < -240 or self.abajo > 240:
                return True

    def decir(self, mensaje, autoeliminar=True):
        nuevo_actor = pilas.actores.Globo(mensaje, self.x, self.y,
                autoeliminar=autoeliminar)
        nuevo_actor.z = self.z - 1
        self.anexar(nuevo_actor)

    def anexar(self, otro_actor):
        self.anexados.append(otro_actor)

    def _eliminar_anexados(self):
        for x in self.anexados:
            x.eliminar()
