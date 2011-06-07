# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.simbolos import *
import eventos

class Control:
    """Representa un control de teclado sencillo.

    Este objeto permite acceder al estado del teclado usando
    atributos.

    Por ejemplo, con este objeto, para saber si el usuario
    está pulsando el direccional hacia la izquierda de
    puede ejecutar::

        if pilas.control.izquierda:
            print 'Ha pulsado hacia la izquierda'
    """

    def __init__(self):
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.boton = False

        eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        eventos.suelta_tecla.conectar(self.cuando_suelta_una_tecla)

    def cuando_pulsa_una_tecla(self, evento):
        self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, True)

    def cuando_suelta_una_tecla(self, evento):
        self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, False)

    def procesar_cambio_de_estado_en_la_tecla(self, codigo, estado):
        mapa = {
            IZQUIERDA: 'izquierda',
            DERECHA: 'derecha',
            ARRIBA: 'arriba',
            ABAJO: 'abajo',
            SELECCION: 'boton',
        }

        if mapa.has_key(codigo):
            setattr(self, mapa[codigo], estado)
