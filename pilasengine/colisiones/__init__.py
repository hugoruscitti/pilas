# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import collections

class Colisiones:
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

        if actor_asociado_1 and actor_asociado_2:
            info_colision = {'actor1': actor_asociado_1,
                             'actor2': actor_asociado_2}
            self._colisiones_en_curso.append(info_colision)

    def actualizar(self):
        """Realiza todas las comprobaciones de colisiones.

        Este método dispara todas las acciones asociadas a las colisiones
        programadas cuando se producen.
        """

        for info_colision in self._colisiones_en_curso:
            actor_1 = info_colision['actor1']
            actor_2 = info_colision['actor2']

            self._ejecutar_colision_programada_si_existe(actor_1, actor_2)

        self._colisiones_en_curso = []

    def _ejecutar_colision_programada_si_existe(self, actor_1, actor_2):
        for (grupo_a, grupo_b, funcion_a_llamar) in self._colisiones_programadas_con_respuesta:
            for a in grupo_a:
                for b in grupo_b:
                    if a in (actor_1, actor_2) and b in (actor_1, actor_2):
                        if not a.esta_eliminado() and not b.esta_eliminado():
                            self.invocar_funcion(funcion_a_llamar, a, b)

    def invocar_funcion(self, funcion, actor1, actor2):
        try:
            funcion(actor1, actor2)
        except TypeError:
            funcion()

    def agregar(self, grupo_a, grupo_b, funcion_a_llamar):
        "Agrega dos listas de actores para analizar _colisiones."

        if not isinstance(grupo_a, list) and not isinstance(grupo_a, collections.MutableSequence):
            grupo_a = [grupo_a]

        if not isinstance(grupo_b, list) and not isinstance(grupo_b, collections.MutableSequence):
            grupo_b = [grupo_b]

        self._colisiones_programadas_con_respuesta.append((grupo_a, grupo_b, funcion_a_llamar))