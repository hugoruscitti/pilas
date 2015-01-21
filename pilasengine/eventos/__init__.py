# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import evento


class Eventos(object):
    """Representa el objeto pilas.eventos, que internamente delega
    todos los metodos conectados a la escena actual.

    Para acceder a este objeto, usar una sentencia como la siguiente:

        >>> pilas.eventos.click_de_mouse.conectar(una_funcion)

    La función enviada como parámetro será invocada cuando el evento
    ocurra. Y se enviará como argumento los datos del evento, por ejemplo:

        >>> def cuando_hace_click(evento):
        ...     print evento.x
        ...     print evento.y
        ...
        >>> pilas.eventos.click_de_mouse.conectar(cuando_hace_click)

    """
    def __init__(self, pilas):
        self.pilas = pilas

    @property
    def click_de_mouse(self):
        """Informa ante la pulsación del mouse.

        :param x: Posición horizontal del mouse.
        :param y: Posición vertical del mouse.
        :param dx: Posición horizontal relativa del mouse.
        :param dy: Posición vertical relativa del mouse.
        :param boton: Botón del mouse que se pulsó (1 - Izquierdo, 2 -
                      Derecho, 4 - Central)
        """
        return self.pilas.escena_actual().click_de_mouse

    @property
    def mueve_camara(self):
        """Informa que ha cambiado la posición de la cámara.

        :param x: Posición horizontal de la cámara.
        :param y: Posición vertical de la cámara.
        :param dx: Movimiento relativo horizontal que sufrió la cámara.
        :param dy: Movimiento relativo vertical que sufrió la cámara.
        """
        return self.pilas.escena_actual().mueve_camara

    @property
    def mueve_mouse(self):
        """Informa que la posición del mouse ha cambiado.

        :param x: Posición horizontal del mouse.
        :param y: Posición vertical del mouse.
        :param dx: Posición horizontal relativa del mouse.
        :param dy: Posición vertical relativa del mouse.
        """
        return self.pilas.escena_actual().mueve_mouse

    @property
    def termina_click(self):
        """Informa cuando la pulsación del mouse termina.

        :param x: Posición horizontal del mouse.
        :param y: Posición vertical del mouse.
        :param dx: Posición horizontal relativa del mouse.
        :param dy: Posición vertical relativa del mouse.
        :param boton: Botón del mouse que se pulsó (1 - Izquierdo, 2 -
                      Derecho, 4 - Central)
        """
        return self.pilas.escena_actual().termina_click

    @property
    def mueve_rueda(self):
        """Indica que cambió la rueda del mouse que se utiliza
        para desplazamiento o scroll.

        :param delta: indica el grado de rotación de la rueda del mouse.
        """
        return self.pilas.escena_actual().mueve_rueda

    @property
    def pulsa_tecla(self):
        """Informa que se ha pulsado una tecla del teclado.

        :param codigo: Codigo de la tecla normalizado,
                       por ejemplo ``simbolos.m``.
        :param es_repeticion: Indica si el evento surgió por repetición de
                              teclado. False indica que es la primer pulsación.
        :param texto: Cadena de texto que indica la tecla pulsada,
                      por ejemplo ``"m"``.
        """
        return self.pilas.escena_actual().pulsa_tecla

    @property
    def suelta_tecla(self):
        """Informa que se ha soltado una tecla del teclado.

        :param codigo: Codigo de la tecla normalizado,
                       por ejemplo ``simbolos.m``.
        :param es_repeticion: Indica si el evento surgió por repetición de
                              teclado. False indica que es la primer pulsación.
        :param texto: Cadena de texto que indica la tecla pulsada,
                      por ejemplo ``"m"``.
        """
        return self.pilas.escena_actual().suelta_tecla

    @property
    def pulsa_tecla_escape(self):
        """Indica que se ha pulsado la tecla ``scape``."""
        return self.pilas.escena_actual().pulsa_tecla_escape

    @property
    def actualizar(self):
        """Se invoca regularmente, 60 veces por segundo."""
        return self.pilas.escena_actual().cuando_actualiza

    @property
    def Evento(self):
        return evento.Evento

