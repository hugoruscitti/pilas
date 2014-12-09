# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import collections
from pilasengine.actores.actor import Actor


class Grupo(collections.MutableSequence):
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
        self.__dict__['pilas'] = pilas
        self.__dict__['_actores'] = []
        self.pilas.log("Creando el grupo", self)
        self.__dict__['etiquetas'] = AgrupadorEtiquetas(self)

    def __setattr__(self, atributo, valor):
        """Este metodo es llamado cuando queremos modificar algun atributo de
        los actores, por ejemplo:

            >>> coches = Coche() * 10 # Creamos un grupo de 10 coches
            >>> coches.velocidad = 100

        Para modificar el valor 'velocidad' a todos los actores del grupo
        """
        self._definir_valor_de(atributo, valor)

    def __getattr__(self, atributo):
        """ Este metodo es llamado cuando queremos ejecutar un metodo
        de los actores, por ejemplo:

            >>> monos = pilas.actores.Mono() * 10
            >>> monos.decir("hola mundo")

        Todos los actores dentro del grupo tratan de ejecutar el metodo 'decir'
         """
        def map_a_todos(*args, **kwargs):
            for actor in self._actores:
                funcion = getattr(actor, atributo)
                funcion(*args, **kwargs)

        return map_a_todos

    def obtener_cantidad_de_actores(self):
        return len(self._actores)

    def __setitem__(self, key, item):
        self._actores[key] = item

    def __getitem__(self, key):
        return self._actores[key]

    def __delitem__(self, key):
        del self._actores[key]

    def __len__(self):
        return len(self._actores)

    def insert(self, i, key):
        self._actores.insert(i, key)

    def sort(self):
        self._actores.sort()

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
        if not isinstance(actor, Actor) and not isinstance(actor, Grupo):
            raise Exception("Solo puede agregar objetos que herenden de la clase Actor o Grupo.")

        if isinstance(actor, Grupo):
            for x in actor:
                self.agregar(x)

            return

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

    def _obtener_valor_de(self, atributo):
        return [(actor.__class__.__name__, getattr(actor, atributo))
                for actor in self._actores]

    def _definir_valor_de(self, atributo, valor):
        for actor in self._actores:
            setattr(actor, atributo, valor)

    def _obtener_espejado(self):
        return self._obtener_valor_de('espejado')

    def _definir_espejado(self, valor):
        self._definir_valor_de('espejado', valor)

    def _obtener_x(self):
        return self._obtener_valor_de('x')

    def _definir_x(self, valor):
        self._definir_valor_de('x', valor)

    def _obtener_y(self):
        return self._obtener_valor_de('y')

    def _definir_y(self, valor):
        self._definir_valor_de('y', valor)

    def _obtener_escala(self):
        return self._obtener_valor_de('escala')

    def _definir_escala(self, valor):
        self._definir_valor_de('escala', valor)

    def _obtener_rotacion(self):
        return self._obtener_valor_de('rotacion')

    def _definir_rotacion(self, valor):
        self._definir_valor_de('rotacion', valor)

    def _obtener_escala_x(self):
        return self._obtener_valor_de('escala_x')

    def _definir_escala_x(self, valor):
        self._definir_valor_de('escala_x', valor)

    def _obtener_escala_y(self):
        return self._obtener_valor_de('escala_y')

    def _definir_escala_y(self, valor):
        self._definir_valor_de('escala_y',  valor)

    def _obtener_transparencia(self):
        return self._obtener_valor_de('transparencia')

    def _definir_transparencia(self, valor):
        self._definir_valor_de('transparencia', valor)

    def _obtener_fijo(self):
        return self._obtener_valor_de('fijo')

    def _definir_fijo(self, valor):
        self._definir_valor_de('fijo', valor)

    def _obtener_izquierda(self):
        return self._obtener_valor_de('izquierda')

    def _definir_izquierda(self, valor):
        self._definir_valor_de('izquierda', valor)

    def _obtener_derecha(self):
        return self._obtener_valor_de('derecha')

    def _definir_derecha(self, valor):
        self._definir_valor_de('derecha', valor)

    def _obtener_abajo(self):
        return self._obtener_valor_de('abajo')

    def _definir_abajo(self, valor):
        self._definir_valor_de('abajo', valor)

    def _obtener_arriba(self):
        return self._obtener_valor_de('arriba')

    def _definir_arriba(self, valor):
        self._definir_valor_de('arriba', valor)

    espejado = property(_obtener_espejado, _definir_espejado, doc="Indica si \
                        se tiene que invertir horizontalmente la imagen de \
                        los actores.")

    x = property(_obtener_x, _definir_x, doc="Define la posición horizontal del\
                 grupo de actores.")

    y = property(_obtener_y, _definir_y, doc="Define la posición vertical del \
                 grupo de  actores.")

    escala = property(_obtener_escala, _definir_escala, doc="Escala de todos \
                      los actores del grupo")

    rotacion = property(_obtener_rotacion, _definir_rotacion, doc="Angulo de \
                        rotación  en grados de (0 a 360) de todos los actores \
                        del grupo")

    escala_x = property(_obtener_escala_x, _definir_escala_x,
                        doc="Escala de tamaño horizontal, 1 es normal, \
                        2 al doble de tamaño etc...")

    escala_y = property(_obtener_escala_y, _definir_escala_y,
                        doc="Escala de tamaño vertical, 1 es normal, 2 al \
                        doble de tamaño etc...")

    transparencia = property(_obtener_transparencia, _definir_transparencia,
                             doc="Define el nivel de transparencia, 0 indica \
                             opaco y 100 la maxima transparencia.")

    fijo = property(_obtener_fijo, _definir_fijo, doc="Indica si los actores \
                    del grupo deben ser independiente a la cámara.")

    izquierda = property(_obtener_izquierda, _definir_izquierda, doc="Establece\
                          el espacio entre la izquierda de los actores del \
                         grupo y el centro de coordenadas del mundo.")

    derecha = property(_obtener_derecha, _definir_derecha, doc="Establece el \
                       espacio entre la derecha de los actores del grupo \
                       y el centro de coordenadas del mundo.")

    abajo = property(_obtener_abajo, _definir_abajo, doc="Establece el espacio \
                     entre la parte inferior de los actores del grupo \
                     y el centro de coordenadas del mundo.")

    arriba = property(_obtener_arriba, _definir_arriba, doc="Establece el \
                      espacio entre la parte superior de los actores del grupo \
                      y el centro de coordenadas del mundo.")

    def aprender(self, habilidad, *k, **kw):
        for actor in self._actores:
            actor.aprender(habilidad, *k, **kw)

    def __repr__(self):
        cantidad = self.obtener_cantidad_de_actores()

        if cantidad == 0:
            detalle = "sin actores"
        elif cantidad == 1:
            detalle = "con un solo actor"
        else:
            detalle = "con %d actores" % (cantidad)

        return "<Un grupo %s>" % (detalle)

class AgrupadorEtiquetas(object):
    """Representa el atributo etiquetas de todos los actores en el grupo."""

    def __init__(self, grupo):
        self.grupo = grupo

    def agregar(self, etiqueta):
        for actor in self.grupo.obtener_actores():
            actor.etiquetas.agregar(etiqueta)

    def __repr__(self):
        etiquetas = []

        for actor in self.grupo.obtener_actores():
            etiquetas += list(actor.etiquetas.obtener_como_lista())

        return str(list(set(etiquetas)))

    def eliminar(self, etiqueta):
        for actor in self.grupo.obtener_actores():
            actor.etiquetas.eliminar(etiqueta)
