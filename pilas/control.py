# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.simbolos import *

__doc__ = """
Módulo pilas.control
====================

"""

class Control(object):
    """Representa un control de teclado sencillo.

    Este objeto permite acceder al estado del teclado usando
    atributos.

    Por ejemplo, con este objeto, para saber si el usuario
    está pulsando el direccional hacia la izquierda de
    puedes ejecutar::

        if pilas.escena_actual().control.izquierda:
            print 'Ha pulsado hacia la izquierda'

    Es decir, si bien Control es una clase, no hace falta
    instanciarla. Ya existe un objeto que se puede consultar
    bajo el nombre ``pilas.escena_actual().control``.

    Entonces, una vez que tienes la referencia para consultar, los
    atributos que tiene este objeto control son::

        izquierda
        derecha
        arriba
        abajo
        boton

    Cada uno de estos atributos te pueden devolver True, o False, indicando
    si el control está pulsado o no.

    Ten en cuenta que este objeto también se puede imprimir usando
    la sentencia ``print``. Esto es útil para ver el estado completo
    del control de una sola vez:

        >>> print pilas.mundo.control
        <Control izquierda: False derecha: False arriba: False abajo: False boton: False>

    También tienes la posibilidad de crearte un control estableciendo las teclas
    personalizadas.
    Para ello debes crearte un diccionario con las claves izquierda, derecha,
    arriba, abajo y boton.
    Con las constantes de pilas.simbolos, puedes asignar una tecla a cada una
    de las entradas del diccionario.
    
    
    >>>    teclas = {pilas.simbolos.a: 'izquierda',
                              pilas.simbolos.d: 'derecha',
                              pilas.simbolos.w: 'arriba',
                              pilas.simbolos.s: 'abajo',
                              pilas.simbolos.ESPACIO: 'boton'}
                
    >>>    mi_control = pilas.control.Control(pilas.escena_actual(), teclas)
    

    Consultando controles desde un actor:

    Una forma habitual de usar los controles, es consultarlos
    directamente desde el codigo de un actor.

    Para consultar los controles para cambiar la posicion horizontal de
    un actor podrías implementar el método ``actualizar``::

        class Patito(pilas.actores.Actor):

            def __init__(self):
                pilas.actores.Actor.__init__(self)
                self.imagen = "patito.png"

            def actualizar(self):
                if pilas.escena_actual().control.izquierda:
                    self.x -= 5
                    self.espejado = True
                elif pilas.escena_actual().control.derecha:
                    self.x += 5
                    self.espejado = False

    .. image:: ../../pilas/data/patito.png
    """

    def __init__(self, escena, mapa_teclado=None):
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.boton = False

        escena.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        escena.suelta_tecla.conectar(self.cuando_suelta_una_tecla)
        
        if mapa_teclado == None:
            self.mapa_teclado = {IZQUIERDA: 'izquierda',
                                  DERECHA: 'derecha',
                                  ARRIBA: 'arriba',
                                  ABAJO: 'abajo',
                                  ESPACIO: 'boton'}
        else:
            self.mapa_teclado = mapa_teclado

    def cuando_pulsa_una_tecla(self, evento):
        self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, True)

    def cuando_suelta_una_tecla(self, evento):
        self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, False)

    def procesar_cambio_de_estado_en_la_tecla(self, codigo, estado):
        if codigo in self.mapa_teclado:
            setattr(self, self.mapa_teclado[codigo], estado)

    def __str__(self):
        return "<Control izquierda: %s derecha: %s arriba: %s abajo: %s boton: %s>" %(
                str(self.izquierda), str(self.derecha), str(self.arriba),
                str(self.abajo), str(self.boton))

    def limpiar(self):
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.boton = False
