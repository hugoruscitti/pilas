# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.comportamientos.comportamiento import Comportamiento

import inspect
import difflib


class Comportamientos(object):
    """Representa la forma de acceso y construcción de los Comportamientos.

    Esta clase representa el objeto creado por pilas que
    se puede acceder escribiendo ``pilas.comportamientos``. Desde aquí
    se puede acceder a los comportamientos pre-diseñados de y anexarlos
    a los actores para que los ejecuten.

    Por ejemplo, para 'hacer' un comportamiento:

        >>> mono = pilas.actores.Mono()
        >>> mono.hacer(pilas.comportamientos.Saltar)

    """
    def __init__(self):
        self._lista_comportamientos_personalizados = []
        self.diccionario_de_comportamientos = {
            "Comportamiento": self.Comportamiento,
            "Proyectil": self.Proyectil,
            "Saltar": self.Saltar,
            "Avanzar": self.Avanzar,
            "Girar": self.Girar,
            "Orbitar": self.Orbitar,
            "OrbitarSobreActor": self.OrbitarSobreActor,
        }
        
        
        for k, v in self.diccionario_de_comportamientos.items():
            self.diccionario_de_comportamientos[k.lower()] = v

    @property
    def Comportamiento(self):
        return self._referencia_comportamiento('comportamiento',
                                               'Comportamiento')

    @property
    def Proyectil(self):
        return self._referencia_comportamiento('proyectil', 'Proyectil')

    @property
    def Saltar(self):
        return self._referencia_comportamiento('saltar', 'Saltar')

    @property
    def Avanzar(self):
        return self._referencia_comportamiento('avanzar', 'Avanzar')

    @property
    def Girar(self):
        return self._referencia_comportamiento('girar', 'Girar')

    @property
    def Orbitar(self):
        return self._referencia_comportamiento('orbitar', 'Orbitar')
    
    @property
    def OrbitarSobreActor(self):
        return self._referencia_comportamiento('orbitar', 'OrbitarSobreActor')

    def _referencia_comportamiento(self, modulo, clase):
        import importlib
        referencia_a_modulo = importlib.import_module(
            'pilasengine.comportamientos.' + modulo)
        referencia_a_clase = getattr(referencia_a_modulo, clase)
        return referencia_a_clase
    
    
    def vincular(self, clase_del_comportamiento):
        # Se asegura de que la clase sea una habilidad.
        if not issubclass(clase_del_comportamiento, Comportamiento):
            mensaje = "Solo se pueden vincular clases que heredan de pilasengine.comportamientos.Comportamiento"
            raise Exception(mensaje)

        # Se asegura de que el comportamiento no fue vinculado anteriormente.
        nombre = clase_del_comportamiento.__name__
        existe = nombre in self._lista_comportamientos_personalizados or nombre in self.diccionario_de_comportamientos.keys()

        if existe:
            mensaje = "Lo siento, ya existe un comportamiento vinculado con el nombre: " + nombre
            raise Exception(mensaje)

        metodo_iniciar = getattr(clase_del_comportamiento, 'iniciar')
        argumentos = inspect.getargspec(metodo_iniciar)

        if not 'receptor' in argumentos.args:
            mensaje = "El metodo %s.iniciar tiene que poder recibir el argumento 'receptor' como primer argumento." %(nombre)
            raise Exception(mensaje)

        # Vincula la clase anexando el metodo constructor.
        setattr(self.__class__, nombre, clase_del_comportamiento)
        self._lista_comportamientos_personalizados.append(nombre)

        self.diccionario_de_comportamientos[nombre.lower()] = getattr(self.__class__, nombre)
        

    def buscar_comportamiento_por_nombre(self, nombre):
        nombre = nombre.lower()

        try:
            return self.diccionario_de_comportamientos[nombre]
        except KeyError:
            posibilidades = self.diccionario_de_comportamientos.keys()
            similar = difflib.get_close_matches(nombre, posibilidades)

            if similar:
                similar = similar[0]
                raise NameError("lo siento, no existe ese comportamiento... quisiste decir '%s' ?" %(similar))
            else:
                raise NameError("lo siento, no existe un comportamiento con el nombre '%s'..." %(nombre))

