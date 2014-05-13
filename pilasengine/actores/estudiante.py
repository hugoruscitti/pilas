# -*- encoding: utf-8 -*-
import inspect

from pilasengine import habilidades
from pilasengine.habilidades import habilidad

class Estudiante(object):
    """Componente que permite a los actores aprender habilidades o realizar comportamientos."""

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

        # Instanciando habilidad para comprobar si el actor la tiene asignada
        if inspect.isclass(classname):
            if issubclass(classname, habilidad.Habilidad):
                _habilidad = classname(self.pilas)
            else:   
                raise Exception('El actor solo puede aprender clases que hereden de pilasengine.habilidades.Habilidad')
        else:
            _habilidad = classname()

        if self.tiene_habilidad(_habilidad):
            self.eliminar_habilidad(_habilidad)
        
        self.agregar_habilidad(_habilidad, *k, **w)

    def agregar_habilidad(self, habilidad, *k, **w):
        """Agrega una habilidad a la lista de cosas que puede hacer un actor.

        :param habilidad: Objeto que representa una habilidad.
        """
        habilidad.iniciar(self, *k, **w)
        self._habilidades.append(habilidad)

    def eliminar_habilidad(self, habilidad):
        """ Elimina una habilidad asociada a un Actor.

        :param classname: Objeto que representa una habilidad.
        """
        referencia_habilidad = self.obtener_habilidad(habilidad)

        if referencia_habilidad:
            self._habilidades.remove(referencia_habilidad)

    def tiene_habilidad(self, habilidad):
        """Comprueba si el actor ha aprendido la habilidad indicada.

        :param classname: Objeto que representa una habilidad.
        :return: Devuelve True si el actor tiene asignada la habilidad
        """
        habilidades_actuales = [habilidad.__class__ for habilidad in self._habilidades]

        return (habilidad.__class__ in habilidades_actuales)

    def tiene_comportamiento(self, classname):
        """Comprueba si el actor tiene el comportamiento indicado.

        :param classname: Referencia a la clase que representa el comportamiento.
        """
        comportamientos_actuales = [comportamiento.__class__ for comportamiento in self.comportamientos]
        return (classname in comportamientos_actuales)

    def obtener_habilidad(self, habilidad):
        """Obtiene la habilidad asociada a un Actor.

        :param habilidad: Objeto que representa una habilidad.
        :return: Devuelve None si no se encontró.
        """
        su_habilidad = None

        for h in self._habilidades:
            if h.__class__ == habilidad.__class__:
                su_habilidad = h
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


