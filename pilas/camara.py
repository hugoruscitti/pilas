# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class Camara(object):
    """Representa el punto de vista de la ventana.

    Los atributos ``x`` e ``y`` indican cual debe ser el
    punto central de la pantalla. Por defecto estos
    valores con (0, 0)."""

    def __init__(self, motor):
        self.motor = motor

    @pilas.utils.interpolable
    def _set_x(self, x):
        pilas.eventos.mueve_camara.send("movimiento de camara", x=x, y=self.y, dx=x-self.x, dy=0)
        pilas.mundo.motor.definir_centro_de_la_camara(x, self.y)

    def _get_x(self):
        x, y = pilas.mundo.motor.obtener_centro_de_la_camara()
        return x

    @pilas.utils.interpolable
    def _set_y(self, y):
        pilas.eventos.mueve_camara.send("movimiento de camara", x=self.x, y=y, dx=0, dy=y-self.y)
        pilas.mundo.motor.definir_centro_de_la_camara(self.x, y)

    def _get_y(self):
        x, y = pilas.mundo.motor.obtener_centro_de_la_camara()
        return y

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)


    def obtener_area_visible(self):
        """Retorna el area del escenario que está visible por la cámara.

        Por ejemplo, si la cámara está en posición inicial, esta
        función podría retornar:

            >>> pilas.mundo.camara.obtener_area_visible()
            (0, 640, 240, -240)

        y si movemos la cámara un poco para la derecha:

            >>> pilas.mundo.camara.x = 100
            >>> pilas.mundo.camara.obtener_area_visible()
            (100, 740, 240, -240)

        Es decir, la tupla representa un rectángulo de la forma::
        
            (izquierda, derecha, arriba, abajo)

        En nuestro caso, el último ejemplo muestra que cuando
        la cámara se mueve a ``x = 100`` el area de pantalla
        visible es ``(izquierda=100, derecha=740, arriba=240, abajo=-240)``.
        ¡ ha quedado invisible todo lo que está a la izquierda de ``x=100`` !

        Esta función es útil para ``despetar`` actores o simplemente


        Si quieres saber si un actor está fuera de la pantalla hay un
        atajo, existe un método llamado ``esta_fuera_de_la_pantalla`` en
        los propios actores:

            >>> mi_actor = pilas.actores.Mono(x=0, y=0)
            >>> mi_actor.esta_fuera_de_la_pantalla()
            False
            >>> pilas.mundo.camara.x == 900
            >>> mi_actor.esta_fuera_de_la_pantalla()
            True
        """
        ancho, alto = pilas.mundo.motor.obtener_area()
        return (self.x - ancho/2, self.x + ancho/2, self.y + alto/2, self.y - alto/2)
