# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades
from pilasengine import utils


class RotarConMouse(habilidades.Habilidad):
    """"Hace que un actor rote con respecto a la posicion del mouse.

    Ejemplo:

        >>> actor.aprender(pilas.habilidades.RotarConMouse,
                           lado_seguimiento='ABAJO')

    """
    def iniciar(self, receptor, lado_seguimiento='ARRIBA'):
        """Inicializa la Habilidad

        :param receptor: La referencia al actor.
        :param lado_seguimiento: Establece el lado del actor que rotará para
                                 estar encarado hacia el puntero del mouse.
        """
        super(RotarConMouse, self).iniciar(receptor)

        self.lados_de_seguimiento = {'ARRIBA': "90",
                                     'ABAJO': "270",
                                     'IZQUIERDA': "180",
                                     'DERECHA': "0"}
        self.pilas.eventos.mueve_mouse.conectar(self.se_movio_el_mouse)
        self.pilas.eventos.actualizar.conectar(self.rotar)
        self.lado_seguimiento = int(self.lados_de_seguimiento[lado_seguimiento.upper()])
        self.raton_x = receptor.x
        self.raton_y = receptor.y

    def se_movio_el_mouse(self, evento):
        self.raton_x = evento.x
        self.raton_y = evento.y

    def rotar(self, evento):
        receptor = (self.receptor.x, self.receptor.y)
        raton = (self.raton_x, self.raton_y)
        angulo = self.pilas.utils.obtener_angulo_entre(receptor, raton)
        self.receptor.rotacion = (angulo) - self.lado_seguimiento
