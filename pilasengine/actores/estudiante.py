# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import collections

from pilasengine import habilidades
from pilasengine import comportamientos


estructura_comportamiento = collections.namedtuple(
                                "Comportamiento",
                                ['objeto', 'args', 'kwargs'])


class Estudiante(object):
    """Componente que permite a los actores aprender habilidades o
    realizar comportamientos.
    """

    def __init__(self):
        """Inicializa el componente."""
        self._habilidades = []
        self.comportamiento_actual = None
        self.comportamientos = []
        self.repetir_comportamientos_por_siempre = False
        self.habilidades = habilidades.ProxyHabilidades(self._habilidades)

    def aprender(self, classname, *k, **w):
        """Comienza a realizar una habilidad indicada por parametros.

        :param classname: Referencia a la clase que representa la habilidad.
        """

        if isinstance(classname, str):
            classname = self.pilas.habilidades.buscar_habilidad_por_nombre(classname)

        if issubclass(classname, habilidades.Habilidad):
            if self.tiene_habilidad(classname):
                self.eliminar_habilidad(classname)

            self.agregar_habilidad(classname, *k, **w)
        else:
            raise Exception('El actor solo puede aprender clases que hereden \
                            de pilasengine.habilidades.Habilidad')


    def agregar_habilidad(self, classname, *k, **w):
        """Agrega una habilidad a la lista de cosas que puede hacer un actor.

        :param habilidad: Referencia a la clase que representa la habilidad.
        """
        habilidad = classname(self.pilas)
        habilidad.iniciar(self, *k, **w)
        self._habilidades.append(habilidad)

    def eliminar_habilidad(self, classname):
        """ Elimina una habilidad asociada a un Actor.

        :param classname: Referencia a la clase que representa la habilidad.
        """
        referencia_habilidad = self.obtener_habilidad(classname)

        if referencia_habilidad:
            self._habilidades.remove(referencia_habilidad)

    def tiene_habilidad(self, classname):
        """Comprueba si el actor ha aprendido la habilidad indicada.

        :param classname: Referencia a la clase que representa la habilidad.
        :return: Devuelve True si el actor tiene asignada la habilidad
        """
        habilidades_actuales = [habilidad.__class__ for habilidad in self._habilidades]

        return (classname in habilidades_actuales)

    def obtener_habilidad(self, classname):
        """Obtiene la habilidad asociada a un Actor.

        :param habilidad: Referencia a la clase que representa la habilidad.
        :return: Devuelve None si no se encontró.
        """
        su_habilidad = None

        if isinstance(classname, str):
            classname = self.pilas.habilidades.buscar_habilidad_por_nombre(classname)

        for h in self._habilidades:
            if h.__class__ == classname:
                su_habilidad = h
                break

        return su_habilidad

    def eliminar_habilidades(self):
        "Elimina todas las habilidades asociadas al actor."
        for h in self._habilidades:
            h.eliminar()

    def actualizar_habilidades(self):
        "Realiza una actualización sobre todas las habilidades."
        for h in self._habilidades:
            h.actualizar()

    def tiene_comportamiento(self, classname):
        """Comprueba si el actor tiene el comportamiento indicado.

        :param classname: Referencia a la clase que representa el
                          comportamiento.
        """
        comportamientos_actuales = [comportamiento.objeto.__class__
                                    for comportamiento in self.comportamientos]
        return (classname in comportamientos_actuales)

    def hacer_luego(self, classname, repetir_por_siempre=False, *args, **kwargs):
        """Define un nuevo comportamiento para realizar al final.

        Los actores pueden tener una cadena de comportamientos, este
        metodo agrega el comportamiento al final de la cadena.

        :param comportamiento: Referencia al comportamiento.
        :param repetir_por_siempre: Si el comportamiento se volverá a ejecutar
                                    luego de terminar.
        """
        print "Este metodo entra en desuso, utilice el metodo 'hacer' en su lugar ..."
        return self.hacer(classname, *args, **kwargs)
    
    def hacer_inmediatamente(self, classname, *args, **kwargs):
        self.eliminar_comportamientos()
        self._adoptar_el_siguiente_comportamiento()
        self.hacer(classname, *args, **kwargs)

    def hacer(self, classname, *args, **kwargs):
        """Define el comportamiento para el actor de manera inmediata.

        :param classname: Referencia al comportamiento a realizar.
        """

        if isinstance(classname, str):
            classname = self.pilas.comportamientos.buscar_comportamiento_por_nombre(classname)

        if issubclass(classname, comportamientos.Comportamiento):
            self._hacer(classname, *args, **kwargs)
        else:
            raise Exception('''El actor solo puede "hacer" clases que hereden
                            de pilasengine.comportamientos.Comportamiento''')

    def _hacer(self, classname, *args, **kwargs):
        comportamiento = estructura_comportamiento(
                            classname(self.pilas), args, kwargs)

        self.comportamientos.append(comportamiento)

    def eliminar_comportamientos(self):
        "Elimina todos los comportamientos que tiene que hacer el actor."

        for c in list(self.comportamientos):
            self.comportamientos.remove(c)

    def actualizar_comportamientos(self):
        "Actualiza la lista de comportamientos"

        termina = None

        if self.comportamiento_actual:
            termina = self.comportamiento_actual.objeto.actualizar()

            if termina:
                if self.repetir_comportamientos_por_siempre:
                    self.comportamientos.insert(0, self.comportamiento_actual)
                self._adoptar_el_siguiente_comportamiento()
        else:
            self._adoptar_el_siguiente_comportamiento()

    def _adoptar_el_siguiente_comportamiento(self):
        """ Obtiene el siguiente comportamiento de la lista de comportamientos
            y ejecuta su método iniciar"""

        if self.comportamientos:
            comportamiento = self.comportamientos.pop(0)
            self.comportamiento_actual = comportamiento
            self.comportamiento_actual.objeto.iniciar(
                self, *self.comportamiento_actual.args,
                **self.comportamiento_actual.kwargs)
        else:
            self.comportamiento_actual = None
