# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


class Etiquetas(object):
    """Representa una lista de etiquetas que tiene un actor.

    Las etiquetas permiten clasificar a los actores e indentificarlos
    al momento de detectar una colision.

    Por ejemplo, para acceder a las etiquetas de una actor
    podemos escribir:

        >>> actor.etiquetas
        ['Mono']
        >>> actor.etiquetas.agregar('enemigo')
        ['Mono', 'enemigo']

    """

    def __init__(self):
        self.lista = []

    def pre_iniciar(self, *k, **kw):
        pass

    def obtener_como_lista(self):
        return self.lista

    def agregar(self, etiqueta):
        if isinstance(etiqueta, str):
            etiqueta = etiqueta.lower()
            if not etiqueta in self.lista:
                self.lista.append(etiqueta)
        else:
            raise Exception("Solo se permiten etiquetas que sean cadenas de texto, has enviado: " + str(etiqueta))

        return self

    def __repr__(self):
        return str(self.lista)

    def contar(self):
        return len(self.lista)

    def eliminar(self, etiqueta):
        if isinstance(etiqueta, str):
            etiqueta = etiqueta.lower()

            if etiqueta in self.lista:
                self.lista.remove(etiqueta)
            else:
                raise Exception("No se encuentra esta etiqueta en el actor")
        else:
            raise Exception("La etiqueta tiene que ser una cadena de texto")

        return self

    def interseccion(self, otra_lista):
        intersectan = []
        for x in otra_lista:
            if x in self.lista:
                intersectan.append(x)
        return intersectan
