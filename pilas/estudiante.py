# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas.utils
import inspect
import sys

class Estudiante:
    """Componente que permite a los actores aprender habilidades o realizar comportamientos."""

    def __init__(self):
        """Inicializa el componente."""
        self._habilidades = []
        self.comportamiento_actual = None
        self.comportamientos = []
        self.repetir_comportamientos_por_siempre = False
        self.habilidades = ProxyHabilidades(self._habilidades)

    def aprender(self, classname, *k, **w):
        """Comienza a realizar una habilidad indicada por parametros.

        :param classname: Referencia a la clase que representa la habilidad.
        """
        if self.tiene_habilidad(classname):
            self.eliminar_habilidad(classname)
            self.agregar_habilidad(classname, *k, **w)
        else:
            self.agregar_habilidad(classname, *k, **w)

    def agregar_habilidad(self, classname, *k, **w):
        """Agrega una habilidad a la lista de cosas que puede hacer un actor.

        :param classname: Referencia a la clase que representa la habilidad.
        """
        objeto_habilidad = classname(self, *k, **w)
        self._habilidades.append(objeto_habilidad)

    def eliminar_habilidad(self, classname):
        """ Elimina una habilidad asociada a un Actor.

        :param classname: Referencia a la clase que representa la habilidad.
        """
        habilidad = self.obtener_habilidad(classname)

        if habilidad:
            self._habilidades.remove(habilidad)

    def tiene_habilidad(self, classname):
        """Comprueba si el actor ha aprendido la habilidad indicada.

        :param classname: Referencia a la clase que representa la habilidad.
        """
        habilidades_actuales = [habilidad.__class__ for habilidad in self._habilidades]
        return (classname in habilidades_actuales)

    def tiene_comportamiento(self, classname):
        """Comprueba si el actor tiene el comportamiento indicado.

        :param classname: Referencia a la clase que representa el comportamiento.
        """
        comportamientos_actuales = [comportamiento.__class__ for comportamiento in self.comportamientos]
        return (classname in comportamientos_actuales)

    def obtener_habilidad(self, classname):
        """Obtiene la habilidad asociada a un Actor.

        :param classname: Referencia a la clase que representa la habilidad.
        :return: Devuelve None si no se encontró.
        """
        su_habilidad = None

        for habilidad in self._habilidades:
            if habilidad.__class__ == classname:
                su_habilidad = habilidad
                break

        return su_habilidad

    def hacer_luego(self, comportamiento, repetir_por_siempre=False, *k, **kw):
        """Define un nuevo comportamiento para realizar al final.

        Los actores pueden tener una cadena de comportamientos, este
        metodo agrega el comportamiento al final de la cadena.

        :param comportamiento: Referencia al comportamiento.
        :param repetir_por_siempre: Si el comportamiento se volverá a ejecutar luego de terminar.
        """

        # El comportamiento se trata de diferente forma si se pasa como instancia o como
        # clase.
        # Se pretende que el comportamiento se asigne de la misma forma que las habilidades
        # actor.hacer_luego(pilas.comportamientos.Orbitar, velocidad=3, direccion="derecha")
        # aunque se conserva la forma antígua de asignar el comportamiento
        # actor.hacer_luego(pilas.comportamientos..Orbitar(velocidad=3, direccion="derecha"))

        if (inspect.isclass(comportamiento)):
            self._hacer_luego(comportamiento,repetir_por_siempre, *k, **kw)
        else:
            self.comportamientos.append(comportamiento)
            self.repetir_comportamientos_por_siempre = repetir_por_siempre

    def _hacer_luego(self, comportamiento, repetir_por_siempre=False, *k, **kw):
        objecto_comportamiento = comportamiento(*k, **kw)
        self.comportamientos.append(objecto_comportamiento)
        self.repetir_comportamientos_por_siempre = repetir_por_siempre


    def hacer(self, comportamiento, *k, **kw):
        """Define el comportamiento para el actor de manera inmediata.

        :param comportamiento: Referencia al comportamiento a realizar.
        """

        # El comportamiento se trata de diferente forma si se pasa como instancia o como
        # clase.
        # Se pretende que el comportamiento se asigne de la misma forma que las habilidades
        # actor.hacer(pilas.comportamientos.Orbitar, velocidad=3, direccion="derecha")
        # aunque se conserva la forma antígua de asignar el comportamiento
        # actor.hacer(pilas.comportamientos..Orbitar(velocidad=3, direccion="derecha"))

        if (inspect.isclass(comportamiento)):
            self._hacer(comportamiento, *k, **kw)
        else:
            self.comportamientos.insert(0, comportamiento)
            self._adoptar_el_siguiente_comportamiento()

    def _hacer(self, comportamiento, *k, **kw):
        objecto_comportamiento = comportamiento(*k, **kw)
        self.comportamientos.insert(0, objecto_comportamiento)
        self._adoptar_el_siguiente_comportamiento()

    def eliminar_habilidades(self):
        "Elimina todas las habilidades asociadas al actor."
        for h in self._habilidades:
            h.eliminar()

    def eliminar_comportamientos(self):
        "Elimina todos los comportamientos que tiene que hacer el actor."
        for c in self.comportamientos:
            c.eliminar()

    def actualizar_habilidades(self):
        "Realiza una actualización sobre todas las habilidades."
        for h in self._habilidades:
            h.actualizar()

    def actualizar_comportamientos(self):
        "Actualiza la lista de comportamientos"
        termina = None

        if self.comportamiento_actual:
            termina = self.comportamiento_actual.actualizar()

            if termina:
                if self.repetir_comportamientos_por_siempre:
                    self.comportamientos.insert(0, self.comportamiento_actual)
                self._adoptar_el_siguiente_comportamiento()
        else:
            self._adoptar_el_siguiente_comportamiento()

    def _adoptar_el_siguiente_comportamiento(self):
        if self.comportamientos:
            self.comportamiento_actual = self.comportamientos.pop(0)
            self.comportamiento_actual.iniciar(self)
        else:
            self.comportamiento_actual = None


class ProxyHabilidades(object):
    """Implementa un intermediario con todas las habilidades del Actor."""

    def __init__(self, habilidades):
        self.habilidades = habilidades

    def __getattr__(self, name):
        su_habilidad = None

        for habilidad in self.habilidades:
            if habilidad.__class__.__name__ == name:
                su_habilidad = habilidad
                break

        if not su_habilidad:
            raise Exception("El actor no tiene asignada la habilidad " + name +
                            ".\n No puede acceder mediante actor.habilidades." + name)

        return su_habilidad
