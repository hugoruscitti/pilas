# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import weakref
import types
import inspect


class Evento():
    """Representa un evento, el cual puede conectar,desconectar
    y emitir funciones o métodos"""

    def __init__(self, nombre):
        self.respuestas = set()
        self.nombre = nombre

    def emitir(self, **evento):
        a_eliminar = []

        for respuesta in set(self.respuestas):
            try:
                respuesta(**evento)
            except Exception, e:
                a_eliminar.append(respuesta)
                raise Exception(e)

        if a_eliminar:
            for x in a_eliminar:
                self.desconectar(x)

    def conectar(self, respuesta, id=None):
        if inspect.isfunction(respuesta):
            self.respuestas.add(ProxyFuncion(respuesta, id))
        elif inspect.ismethod(respuesta):
            self.respuestas.add(ProxyMetodo(respuesta, id))
        else:
            raise ValueError("Solo se permite conectar nombres de funciones o \
                             metodos.")

    def desconectar(self, respuesta):
        try:
            self.respuestas.remove(respuesta)
        except:
            raise ValueError("La funcion indicada no estaba agregada como \
                             respuesta del evento.")

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
            ## WARN TODO: informar que el metodo ha dejado de existir
            #raise ReferenceError("El metodo ha dejado de existir")
            return
        elif self.inst is not None:
            mtd = types.MethodType(self.func, self.inst())
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
