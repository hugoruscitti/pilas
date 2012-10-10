# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
#
# Este sistema de eventos está basado en:
#
#     http://stackoverflow.com/questions/1092531/event-system-in-python
#

import weakref
import new
import inspect
import pilas

__doc__ = """
Módulo pilas.evento
===================

"""

class Evento():

    def __init__(self, nombre):
        self.respuestas = set()
        self.nombre = nombre

    def emitir(self, **evento):
        a_eliminar = []

        for respuesta in set(self.respuestas):
            try:
                respuesta(**evento)
            except ReferenceError:
                a_eliminar.append(respuesta)

        if a_eliminar:
            for x in a_eliminar:
                self.desconectar(x)

    def conectar(self, respuesta, id=None):
        if inspect.isfunction(respuesta):
            self.respuestas.add(ProxyFuncion(respuesta, id))
        elif inspect.ismethod(respuesta):
            self.respuestas.add(ProxyMetodo(respuesta, id))
        else:
            raise ValueError("Solo se permite conectar nombres de funciones o metodos.")

    def desconectar(self, respuesta):
        try:
            self.respuestas.remove(respuesta)
        except:
            raise ValueError("La funcion indicada no estaba agregada como respuesta del evento.")

    def desconectar_por_id(self, id):
        a_eliminar = []
        for respuesta in self.respuestas:
            if respuesta.id == id:
                a_eliminar.append(respuesta)

        for x in a_eliminar:
            self.desconectar(x)

    def esta_conectado(self):
        return len(self.respuestas) > 0

    def imprimir_funciones_conectadas(self):
        if not self.esta_conectado():
            print "\t << sin funciones conectadas >>"
        else:
            for x in self.respuestas:
                print "\t +", x.nombre, " en ", x.receptor


class AttrDict(dict):
    """Envoltorio para que el diccionario de eventos
    se pueda acceder usando como si tuviera attributos
    de objeto.

    Por ejemplo, con esta clase es posible que un diccionario
    se pueda usar así:

        >>> b = AttrDict({'x': 123})
        >>> b.x
        123
        >>> b['x']
        123
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        return self[name]


class ProxyFuncion(object):
    """
    Representa a una función de repuesta pero usando
    una referencia débil.
    """

    def __init__(self, cb, id):
        self.funcion = weakref.ref(cb)
        self.id = id
        self.nombre = str(cb)
        self.receptor = str('modulo actual')

    def __call__(self, **evento):
        f = self.funcion()

        if f is not None:
            f(AttrDict(evento))
        else:
            raise ReferenceError("La funcion dejo de existir")


class ProxyMetodo(object):
    """
    Permite asociar funciones pero con referencias débiles, que no
    incrementan el contador de referencias.

    Este proxy funciona tanto con funciones como con métodos enlazados
    a un objeto.

    @organization: IBM Corporation
    @copyright: Copyright (c) 2005, 2006 IBM Corporation
    @license: The BSD License
    """

    def __init__(self, cb, id):
        try:
            try:
                self.inst = weakref.ref(cb.im_self)
            except TypeError:
                self.inst = None
            self.func = cb.im_func
            self.klass = cb.im_class
        except AttributeError:
            self.inst = None
            try:
                self.func = cb.im_func
            except AttributeError:
                self.func = cb

            self.klass = None

        self.id = id
        self.nombre = str(cb.__name__)
        self.receptor = self.klass

    def __call__(self, **evento):
        if self.inst is not None and self.inst() is None:
            raise ReferenceError("El metodo ha dejado de existir")
        elif self.inst is not None:
            mtd = new.instancemethod(self.func, self.inst(), self.klass)
        else:
            mtd = self.func

        return mtd(AttrDict(evento))

    def __eq__(self, other):
        try:
            return self.func == other.func and self.inst() == other.inst()
        except Exception:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ProxyEventos(object):
    """Representa el objeto pilas.evento, que internamente delega todos los metodos
    conectados a la escena actual.

    Para acceder a este objeto, usar una sentencia como la siguiente:

        >>> pilas.eventos.click_de_mouse.conectar(una_funcion)

    Este objeto permite que la API de pilas no cambie notoriamente con la inclusion
    de las nuevas escenas.
    """

    @property
    def click_de_mouse(self):
        """Informa ante la pulsación del mouse.

        :param x: Posición horizontal del mouse.
        :param y: Posición vertical del mouse.
        :param dx: Posición horizontal relativa del mouse.
        :param dy: Posición vertical relativa del mouse.
        """
        return pilas.escena_actual().click_de_mouse

    @property
    def mueve_camara(self):
        return pilas.escena_actual().mueve_camara

    @property
    def mueve_mouse(self):
        return pilas.escena_actual().mueve_mouse

    @property
    def termina_click(self):
        """Informa cuando la pulsación del mouse termina.

        :param x: Posición horizontal del mouse.
        :param y: Posición vertical del mouse.
        :param dx: Posición horizontal relativa del mouse.
        :param dy: Posición vertical relativa del mouse.
        """
        return pilas.escena_actual().termina_click

    @property
    def mueve_rueda(self):
        return pilas.escena_actual().mueve_rueda

    @property
    def pulsa_tecla(self):
        return pilas.escena_actual().pulsa_tecla

    @property
    def suelta_tecla(self):
        return pilas.escena_actual().suelta_tecla

    @property
    def pulsa_tecla_escape(self):
        return pilas.escena_actual().pulsa_tecla_escape

    @property
    def cuando_actualiza(self):
        return pilas.escena_actual().cuando_actualiza

    @property
    def log(self):
        return pilas.escena_actual().log
