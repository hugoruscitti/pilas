# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor
import Image
import os
class Fondo(Actor):

    def __init__(self, imagen):
        self._eliminar_el_fondo_de_pantalla_actual()
        Actor.__init__(self, imagen)
        self.z = 1000

    def _eliminar_el_fondo_de_pantalla_actual(self):
        fondos = [x for x in pilas.escena_actual().actores if x.es_fondo()]
        a_eliminar = []
        for f in fondos:
            a_eliminar.append(f)

        for fondo in a_eliminar:
            fondo.eliminar()

    def es_fondo(self):
        return True


class Volley(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/volley.jpg")

class Nubes(Fondo):
    "Muestra un fondo celeste con nubes."

    def __init__(self):
        Fondo.__init__(self, "fondos/nubes.png")

class Pasto(Fondo):
    "Muestrak una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/pasto.png")

class Selva(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/selva.jpg")


class Tarde(Fondo):
    "Representa una escena de fondo casi naranja."

    def __init__(self):
        Fondo.__init__(self, "fondos/tarde.jpg")
        self.y = 40


class Espacio(Fondo):
    "Es un espacio con estrellas."

    def __init__(self):
        Fondo.__init__(self, "fondos/espacio.jpg")

class Noche(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/noche.jpg")

class Color(Fondo):
    "Pinta todo el fondo de un color uniforme."

    def __init__(self, color):
        Fondo.__init__(self, "invisible.png")
        self.color = color
        self.lienzo = pilas.imagenes.cargar_lienzo()

    def dibujar(self, motor):
        if self.color:
            self.lienzo.pintar(motor, self.color)

class FondoPersonalizado(Fondo):
    "Permite definir una imágen como fondo de un escena y analizar la opacidad de sus pixeles"
    def __init__(self, imagen):
        Fondo.__init__(self, imagen)
        self.imagenFndo =  Image.open(imagen)
      #  pilas.mundo.get_gestor().escena_actual().set_fondo(self)
        pilas.mundo.gestor_escenas.escena_actual().set_fondo(self)


    def informacion_de_un_pixel(self, x, y):
        return self.imagenFndo.getpixel( (x,y) )

    def dimension_fondo(self):
        return self.imagenFndo.size

class Desplazamiento(Fondo):
    """Representa un fondo formado por varias capas (o actores).

    En fondo de este tipo, ayuda a generar un efecto de profundidad,
    de perspectiva en tres dimensiones.
    """

    def __init__(self, ciclico=True):
        "Inicia el objeto, dando la opción de simular que el fondo es infinitio"

        Fondo.__init__(self, "invisible.png")
        self.posicion = 0
        self.posicion_anterior = 0
        self.capas = []
        self.velocidades = {}
        self.escena.mueve_camara.conectar(self.cuando_mueve_camara)
        self.ciclico = ciclico

        if ciclico:
            self.capas_auxiliares = []

    def agregar(self, capa, velocidad=1):
        x, _, _, y = pilas.utils.obtener_bordes()
        capa.fijo = True
        capa.izquierda = x

        self.capas.append(capa)
        self.velocidades[capa] = velocidad

        if self.ciclico:
            copia = capa.duplicar()
            copia.y = capa.y
            copia.z = capa.z
            copia.fijo = True
            copia.imagen = capa.imagen
            self.capas_auxiliares.append(copia)
            copia.izquierda = capa.derecha
            self.velocidades[copia] = velocidad

    def actualizar(self):
        if self.posicion != self.posicion_anterior:
            dx = self.posicion - self.posicion_anterior
            self.mover_capas(dx)
            self.posicion_anterior = self.posicion

    def cuando_mueve_camara(self, evento):
        dx = evento.dx

        # Hace que las capas no se desplacen naturalmente
        # como todos los actores.
        #for x in self.capas:
        #    x.x += dx

        # aplica un movimiento respetando las velocidades.
        self.mover_capas(dx)

    def mover_capas(self, dx):
        for capa in self.capas:
            capa.x -= dx * self.velocidades[capa]

        if self.ciclico:
            for capa in self.capas_auxiliares:
                capa.x -= dx * self.velocidades[capa]

        # Resituar capa cuando se sale del todo de la ventana
        ancho = pilas.mundo.motor.ventana.width()
        if self.ciclico:
            for capa in self.capas:
                if capa.derecha < -ancho / 2:
                    capa.izquierda = \
                        self.capas_auxiliares[self.capas.index(capa)].derecha
            for capa in self.capas_auxiliares:
                if capa.derecha < -ancho / 2:
                    capa.izquierda = \
                        self.capas[self.capas_auxiliares.index(capa)].derecha

class Plano(Fondo):

    def __init__(self):
        Fondo.__init__(self,"plano.png")
        imagen = os.path.abspath(os.path.dirname(__file__)) + "/data/plano.png"
        self.imagenFndo = Image.open(imagen)
    
    def informacion_de_un_pixel(self, x, y):
        # Porque el fondo esde un sólo color. Entonces no mporta el valor del pixel
        return self.imagenFndo.getpixel( (1,1) )

    def dimension_fondo(self):
        # No importa el tamaño de la imagen del fondo, porque tiene el mismo color en todos lados.
        return (0, 0) 

    
    def dibujar(self, painter):
        painter.save()
        x = pilas.mundo.motor.camara_x
        y = -pilas.mundo.motor.camara_y

        ancho, alto = pilas.mundo.obtener_area()
        painter.drawTiledPixmap(0, 0, ancho, alto, self.imagen._imagen, x % 30, y % 30)

        painter.restore()

    def esta_fuera_de_la_pantalla(self):
        return False

class Capa():

    def __init__(self, imagen, x, y, velocidad):
        self.imagen = pilas.imagenes.cargar(imagen)
        self.x = x
        self.y = y
        self.velocidad = velocidad

    def dibujar_tiled_horizontal(self, painter, ancho, alto):
        dx = self.x% self.imagen.ancho()
        dy = 0
        painter.drawTiledPixmap(0, self.y, ancho, self.imagen.alto(), self.imagen._imagen,
                                abs(dx) % self.imagen.ancho(), dy % self.imagen.alto())

    def mover_horizontal(self, dx):
        self.x += dx * self.velocidad

class DesplazamientoHorizontal(Fondo):
    """
    Representa un fondo con desplazamiento horizontal y repetido.

    Este tipo de fondo es ideal para animaciones y juegos donde
    el fondo se puede repetir una y otra vez. Por ejemplo en un juego
    de carreras horizontal o de naves.

    El fondo inicialmente no tiene apariencia, pero se pueden agregar
    capas, cada una con su propia velocidad y posición.

    Por ejemplo, si queremos simular un fondo con 3 capas, una lejana
    con estrellas, y luego dos capas mas cercanas con arboles y arbustos
    podemos escribir:

        >>> fondo = pilas.fondos.DesplazamientoHorizontal()
        >>> fondo.agregar("estrellas.png", 0, 0, 0)
        >>> fondo.agregar("arboles_lejanos.png", 0, 0, 1)
        >>> fondo.agregar("arbustos_cercanos.png", 0, 0, 2)

    El primer argumento del método agregar es la imagen que se tiene
    que repetir horizontalmente. Luego viene la posición 'x' e 'y'. Por
    último el valor numérico es la velocidad de movimiento que tendría
    esa capa.

    Un valor grande de velocidad significa que la capa se moverá
    mas rápido que otras ante un cambio de posición en la cámara. Por
    ejemplo, la capa que tiene velocidad 2 significa que se moverá 2 pixels
    hacia la izquierda cada vez que la cámara mire 2 pixel hacia la derecha.

    Si la capa tiene velocidad 0 significa que permanecerá inamovible al movimiento
    de la cámara.
    """

    def __init__(self):
        self.capas = []
        pilas.actores.Actor.__init__(self, "invisible.png")
        self.escena.mueve_camara.conectar(self.cuando_mueve_camara)
        self.z = 1000

    def dibujar(self, painter):
        painter.save()
        ancho, alto = pilas.mundo.obtener_area()

        for capa in self.capas:
            capa.dibujar_tiled_horizontal(painter, ancho, alto)

        painter.restore()

    def agregar(self, imagen, x=0, y=0, velocidad=0):
        nueva_capa = Capa(imagen, x, y, velocidad)
        self.capas.append(nueva_capa)

    def cuando_mueve_camara(self, evento):
        for capa in self.capas:
            capa.mover_horizontal(evento.dx)

    def esta_fuera_de_la_pantalla(self):
        return False
