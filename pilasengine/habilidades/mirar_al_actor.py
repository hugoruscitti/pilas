# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import habilidades
from pilasengine import utils


class MirarAlActor(habilidades.Habilidad):
    """"Hace que un actor rote para mirar hacia otro actor."""

    def iniciar(self, receptor, actor_a_seguir, lado_seguimiento='ARRIBA'):
        """Inicializa la habilidad.

        :param receptor: Actor que aprenderá la habilidad.
        :param actor_a_seguir : Actor al que se desea seguir con la mirada.
        :param lado_seguimiento: Establece el lado del actor que rotará para
                                estar encarado hacia el actor que desea vigilar.
        """
        super(MirarAlActor, self).iniciar(receptor)
        self.lados_de_seguimiento = {'ARRIBA': "90",
                                     'ABAJO': "270",
                                     'IZQUIERDA': "180",
                                     'DERECHA': "0"}
        self.pilas.eventos.actualizar.conectar(self.rotar)
        self.lado_seguimiento = int(self.lados_de_seguimiento[lado_seguimiento])
        self.actor_a_seguir = actor_a_seguir

    def rotar(self, evento):
        receptor = (self.receptor.x, self.receptor.y)
        actor_a_seguir = (self.actor_a_seguir.x, self.actor_a_seguir.y)

        angulo = utils.obtener_angulo_entre(receptor, actor_a_seguir)

        self.receptor.rotacion = angulo - self.lado_seguimiento
