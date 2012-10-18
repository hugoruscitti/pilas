# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import pilas.pytweener

class Interpolacion(object):
    """Representa una interpolacion, que pasa por varios puntos clave.

    Las interpolacione se utilizan para realizar movimientos de
    actores en la pantalla. O simplemente para cambiar el
    estado de un actor de un punto a otro, por ejemplo, de 0 a 360
    grados de manera gradual.

    Todo objeto de interpolaciones se puede asignar directamente a
    una propiedad de un actor. Por ejemplo:

        actor.rotation = pilas.interpolations.Lineal(400)

    note que hay un atajo para usar estos objetos, es mejor
    utilizar directamente una sentencias como la que sigue::

        actor.rotation = pilas.interpolate(360)
    """
    def __init__(self, values, duration, delay):
        """Inicializa la interpolación.

        ``values`` tiene que ser una lista con todos los puntos
        por los que se quiere adoptar valores y ``duration`` es la cantidad
        de segundos que deben tomarse para realizar la interpolación.
        """
        self.values = values
        self.duration = duration
        self.delay = delay

    def apply(self, target, function, type):
        """Aplica la interpolación a un actor usando un método.

        Esta funcionalidad se utiliza para que toda interpolación
        se pueda acoplar a un actor.

        La idea es contar con la interpolación, un actor y luego
        ponerla en funcionamiento::

            mi_interpolacion.apply(mono, set_rotation)

        de esta forma los dos objetos están y seguirán estando
        desacoplados."""

        import pilas

        # Tiempo que se debe invertir para hacer cada interpolacion
        # individual.
        step = self.duration / float(len(self.values))
        step *= 1000.0

        # En base a la funcion busca el getter que le dara
        # el valor inicial.
        getter = function.replace('set_', 'get_')
        function_to_get_value = getattr(target, getter)
        fist_value = function_to_get_value()

        # Le indica al objeto que tiene que hacer para cumplir
        # con cada paso de la interpolacion.
        for index, value in enumerate(self.values):
            pilas.escena_actual().tweener.addTweenNoArgs(target, function=function, 
                    initial_value=fist_value,
                    value=value, 
                    tweenDelay=self.delay * 1000.0 + (index * step),
                    tweenTime=step,
                    tweenType=type)
            # El siguiente valor inicial sera el que ha alcanzado.
            fist_value = value

class Lineal(Interpolacion):
    "Representa una interpolación lineal."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return Lineal(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Linear.easeNone) 

class AceleracionGradual(Interpolacion):
    "Representa una interpolación con aceleración gradual."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return AceleracionGradual(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Cubic.easeIn) 

class DesaceleracionGradual(Interpolacion):
    "Representa una interpolación con aceleración gradual."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return DesaceleracionGradual(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Cubic.easeOut) 

class ReboteInicial(Interpolacion):
    "Representa una interpolación con rebote."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return ReboteInicial(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Bounce.easeIn) 

class ReboteFinal(Interpolacion):
    "Representa una interpolación con rebote."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return ReboteFinal(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Bounce.easeOut) 

class ElasticoInicial(Interpolacion):
    "Representa una interpolación con rebote."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return ReboteInicial(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Elastic.easeIn) 


class ElasticoFinal(Interpolacion):
    "Representa una interpolación con rebote."

    def __init__(self, values, duration, delay):
        Interpolacion.__init__(self, values, duration, delay)

    def __neg__(self):
        "Retorna la interpolación inversa a la original."
        new_values = list(self.values)
        new_values.reverse()
        return ReboteInicial(new_values, self.duration, self.delay)

    def apply(self, target, function):
        Interpolacion.apply(self, target, function, pilas.pytweener.Easing.Elastic.easeOut) 
