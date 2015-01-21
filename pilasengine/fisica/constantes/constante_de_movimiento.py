# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
from pilasengine import utils

class ConstanteDeMovimiento():
    """Representa una constante de movimiento para el mouse."""

    def __init__(self, pilas, figura):
        """Inicializa la constante.

        :param pilas: instancia de pilas
        :param figura: Figura a controlar desde el mouse.
        """
        self.pilas = pilas
        mundo = pilas.escena_actual().fisica.mundo
        punto_captura = utils.convertir_a_metros(figura.x), utils.convertir_a_metros(figura.y)
        self.cuerpo_enlazado = mundo.CreateBody()
        self.constante = mundo.CreateMouseJoint(bodyA=self.cuerpo_enlazado,
                                                bodyB=figura._cuerpo,
                                                target=punto_captura,
                                                maxForce=1000.0*figura._cuerpo.mass)

        figura._cuerpo.awake = True

    def mover(self, x, y):
        """Realiza un movimiento de la figura.

        :param x: Posición horizontal.
        :param y: Posición vertical.
        """
        self.constante.target = (utils.convertir_a_metros(x), utils.convertir_a_metros(y))

    def eliminar(self):
        # Si se intenta destruir un Joint de un cuerpo que ya no existe, se cierra
        # la aplicación.
        self.pilas.escena_actual().fisica.mundo.DestroyBody(self.cuerpo_enlazado)
