# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilasengine
from pilasengine.actores.actor import Actor


class Grupo(object):
    """
    Representa un grupo que puede almacenar actores.

    Los grupos pueden ser útiles para clasificar y organizar
    _actores dentro de un juego. Por ejemplo, todas las naves
    en un grupo, los enemigos en otro grupo y las estrellas
    en otro etc.

    Para crear un grupo y asignarle un actor podemos escribir:

        >>> grupo = pilas.actores.Grupo()
        >>> actor = pilas.actores.Actor()
        >>> grupo.agregar(actor)

    """

    def __init__(self, pilas):
        self.pilas = pilas
        self.pilas.log("Creando el grupo", self)
        self._actores = []

    def obtener_cantidad_de_actores(self):
        return len(self._actores)

    def eliminar(self, actor):
        """Agrega el actor a una lista para eliminarlo mas tarde."""

        if actor in self._actores:
            self._actores.remove(actor)
            actor.eliminar_del_grupo(self)
            self.pilas.log("Eliminando el actor", actor, "del grupo", self)
        else:
            raise Exception("No se puede eliminar el actor porque no \
                            está en el grupo.")

    def agregar(self, actor):
        if not isinstance(actor, Actor):
            raise Exception("Solo puede agregar objetos que herenden de \
                            actor a un Grupo.")

        if actor not in self._actores:
            self.pilas.log("Agregando el actor", actor, "al grupo", self)
            self._actores.append(actor)
            self.pilas.log("Haciendo que el actor", actor,
                           "tenga una referencia al", self)
            actor.agregar_al_grupo(self)
        else:
            raise Exception("No se agrega al actor porque ya estába en \
                            este grupo")

    def obtener_actores(self, fijos=None, sin_padre=False):
        """Retorna una lista de actores.

        El argumento fijos sirve para filtrar los actores. Si se
        especifica True solo se retornan los actores fijos, en cambio
        con False se retornan los actores normales.
        """
        if fijos in [True, False]:
            if sin_padre:
                return [x for x in self._actores if x.fijo == fijos and not x.padre]
            else:
                return [x for x in self._actores if x.fijo == fijos]
        else:
            return list(self._actores)

    def __repr__(self):
        cantidad = self.obtener_cantidad_de_actores()

        if cantidad == 0:
            detalle = "sin actores"
        elif cantidad == 1:
            detalle = "con un solo actor"
        else:
            detalle = "con %d actores" % (cantidad)

        return "<Un grupo %s>" % (detalle)