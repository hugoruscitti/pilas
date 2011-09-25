# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import random

class Grupo(list):
    """Un grupo es un contenedor que funciona como una lista normal, pero mejorada.

    Los grupos pueden contener actores, y permite que a todos los actores
    se los pueda tratar como uno.

    Por ejemplo si tienes un contenedor con 20 actores, podrías ampliar
    el tamaño de todos ellos juntos usando la sentencia::

            grupo = pilas.atajos.fabricar(pilas.actores.Mono, 20)
            grupo.escala = 2

    """

    def __getattr__(self, attr):
        """Esta funcion se asegura de que cada vez que se invoque a un metodo
        del grupo, en realidad, el grupo va a invocar a ese metodo pero
        en todos sus elementos. Algo asi como un map."""

        def map_a_todos(*k, **kw):
            for a in self:
                funcion = getattr(a, attr)
                funcion(*k, **kw)

        return map_a_todos

    def __setattr__(self, atributo, valor):
        for a in self:
            setattr(a, atributo, valor)

    def desordenar(self):
        for a in self:
            a.x = random.randint(-300, 300)
            a.y = random.randint(-200, 200)

    def limpiar(self):
        eliminar = list(self)
        for e in eliminar:
            e.eliminar()
