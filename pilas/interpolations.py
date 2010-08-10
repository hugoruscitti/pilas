# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

class Interpolation:
    """Representa una interpolacion, que va de un numero a otro.

    Las interpolacione se utilizan para realizar movimientos de
    actores en la pantalla. O simplemente para cambiar el
    estado de un actor de un punto a otro, por ejemplo, de 0 a 360
    grados de manera gradual.

    Todo objeto de interpolaciones se puede asignar directamente a
    una propiedad de un actor. Por ejemplo:

        actor.rotation = pilas.interpolations.Linear(0, 400)

    note que hay un atajo para usar estos objetos, es mejor
    utilizar directamente una sentencias como la que sigue::

        actor.rotation = pilas.interpolate(0, 360)
    """



class Linear(Interpolation):

    def __init__(self, from_value, to_value, duration):
        self.from_value = from_value
        self.to_value = to_value
        self.duration = duration

    def __neg__(self):
        return Linear(self.to_value, self.from_value, self.duration)

