# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import collections
import pilasengine

import inspect

class Colisiones(object):
    "Administra todas las _colisiones entre actores."

    def __init__(self, pilas, escena):
        self.pilas = pilas
        self.escena = escena

        # Esta lista contiene elementos de la forma:
        #
        #    (grupo_o_actor_A, grupo_o_actor_B, funcion_de_respuesta)
        #
        # y sus elementos los gestiona el método "agregar".
        self._colisiones_programadas_con_respuesta = []
        self._colisiones_programadas_entre_etiquetas_con_respuesta = []

        # Las colisiones en curso guarda
        self._colisiones_en_curso = []
        self._lista = []

    def notificar_colision(self, fixture_1, fixture_2):
        """Se invoca automáticamente desde el componente Fisica.

        Internamente, el motor de física tiene un objeto llamado
        ContactListener (en el archivo 'fisica/contact_listener.py').
        """
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)

        figura_1 = fixture_1.userData.get('figura', None)
        figura_2 = fixture_2.userData.get('figura', None)

        info_colision = {'actor1': actor_asociado_1,
                         'actor2': actor_asociado_2,
                         'figura1': figura_1,
                         'figura2': figura_2,
                         'fixture1': fixture_1,
                         'fixture2': fixture_2}
        self._colisiones_en_curso.append(info_colision)

    def obtener_cantidad_de_colisiones(self):
        return len(self._colisiones_en_curso)

    def limpiar(self):
        self._colisiones_en_curso = []

    def actualizar(self):
        """Realiza todas las comprobaciones de colisiones.

        Este método dispara todas las acciones asociadas a las colisiones
        programadas cuando se producen.
        """

        for info_colision in self._colisiones_en_curso:
            if info_colision['actor1']:
                actor_1 = info_colision['actor1']
            else:
                actor_1 = info_colision['figura1']

            if info_colision['actor2']:
                actor_2 = info_colision['actor2']
            else:
                actor_2 = info_colision['figura2']

            self._ejecutar_colision_programada_si_existe(actor_1, actor_2)
            self._ejecutar_colisiones_entre_etiquetas_si_existe(actor_1, actor_2)

        self._colisiones_en_curso = []

    def _ejecutar_colision_programada_si_existe(self, actor_1, actor_2):
        for (grupo_a, grupo_b, funcion_a_llamar) in self._colisiones_programadas_con_respuesta:
            for a in grupo_a:
                for b in grupo_b:
                    if a in (actor_1, actor_2) and b in (actor_1, actor_2):
                        if not a.esta_eliminado() and not b.esta_eliminado():
                            self.invocar_funcion(funcion_a_llamar, a, b)

    def _ejecutar_colisiones_entre_etiquetas_si_existe(self, actor_1, actor_2):
        for (grupo_a, grupo_b, funcion_a_llamar) in self._colisiones_programadas_entre_etiquetas_con_respuesta:
            # grupo_a = ['Mono']
            # grupo_b = ['item', 'ememigos']
            if actor_1.etiquetas.interseccion(grupo_a) and actor_2.etiquetas.interseccion(grupo_b):
                self.invocar_funcion(funcion_a_llamar, actor_1, actor_2)
            elif actor_2.etiquetas.interseccion(grupo_a) and actor_1.etiquetas.interseccion(grupo_b):
                self.invocar_funcion(funcion_a_llamar, actor_2, actor_1)

    def invocar_funcion(self, funcion, actor1, actor2):
        if inspect.ismethod(funcion):
            if funcion.func_code.co_argcount == 3:
                funcion(actor1, actor2)
            else:
                funcion()
        else:
            if funcion.func_code.co_argcount == 2:
                funcion(actor1, actor2)
            else:
                funcion()

    def agregar(self, grupo_a, grupo_b, funcion_a_llamar):
        "Agrega dos listas de actores para analizar _colisiones."

        # Se asegura que el primer parámetro se convierta en una lista si
        # es solo un elemento.
        if not isinstance(grupo_a, list) and not isinstance(grupo_a, collections.MutableSequence):
            grupo_a = [grupo_a]

        # Se asegura que el primer parámetro se convierta en una lista si
        # es solo un elemento.
        if not isinstance(grupo_b, list) and not isinstance(grupo_b, collections.MutableSequence):
            grupo_b = [grupo_b]

        # Se asegura de que se llame con etiquetas o actores, pero
        # sin mezclar.
        todos = list(grupo_a) + list(grupo_b)
        cantidad_total = len(todos)
        cantidad_actores, cantidad_etiquetas, cantidad_figuras = self._contar_tipos_de_datos(todos)

        if funcion_a_llamar and not callable(funcion_a_llamar):
            raise Exception(u"El tercer parámetro debe ser una función.")

        if cantidad_total == cantidad_actores:
            self._colisiones_programadas_con_respuesta.append((grupo_a, grupo_b, funcion_a_llamar))
        elif cantidad_total == cantidad_etiquetas:
            grupo_a = self._convertir_en_lista_de_cadenas(grupo_a)
            grupo_b = self._convertir_en_lista_de_cadenas(grupo_b)
            self._colisiones_programadas_entre_etiquetas_con_respuesta.append((grupo_a, grupo_b, funcion_a_llamar))
        elif cantidad_total == cantidad_figuras:
            self._colisiones_programadas_con_respuesta.append((grupo_a, grupo_b, funcion_a_llamar))
        else:
            raise Exception("Las colisiones solo se permiten entre actores o entre etiquetas, pero sin mezclar.")

    def _convertir_en_lista_de_cadenas(self, grupo):
        lista = []

        for x in grupo:
            lista.append(x.lower())

        return lista

    def _contar_tipos_de_datos(self, colecciones):
        """Toma la lista de actores o etiquetas y cuenta cuantas hay de cada tipo."""

        cantidad_actores = 0
        cantidad_etiquetas = 0
        cantidad_figuras = 0

        for x in colecciones:
            if isinstance(x, str):
                cantidad_etiquetas += 1
            elif isinstance(x, pilasengine.actores.Actor):
                cantidad_actores += 1
            elif isinstance(x, pilasengine.fisica.figura.Figura):
                cantidad_figuras += 1

        return cantidad_actores, cantidad_etiquetas, cantidad_figuras
