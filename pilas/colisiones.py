# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import utils
import pilas

class Colisiones:
    "Administra todas las colisiones entre actores."

    def __init__(self):
        self.colisiones = []

    def verificar_colisiones(self):
        for x in self.colisiones:
            self._verificar_colisiones_en_tupla(x)

    def _verificar_colisiones_en_tupla(self, tupla):
        "Toma dos grupos de actores y analiza colisiones entre ellos."
        (grupo_a, grupo_b, funcion_a_llamar) = tupla

        for a in grupo_a:
            for b in grupo_b:
                try:

                    if id(a) != id(b) and utils.colisionan(a, b):
                        funcion_a_llamar(a, b)

                        # verifica si alguno de los dos objetos muere en la colision.
                        if a not in pilas.actores.todos:
                            if a in grupo_a:
                                list.remove(grupo_a, a)

                        if b not in pilas.actores.todos:
                            if b in grupo_b:
                                list.remove(grupo_b, b)
                except Exception as e:
                    list.remove(grupo_a, a)
                    raise e

    def agregar(self, grupo_a, grupo_b, funcion_a_llamar):
        "Agrega dos listas de actores para analizar colisiones."

        if not isinstance(grupo_a, list):
            grupo_a = [grupo_a]

        if not isinstance(grupo_b, list):
            grupo_b = [grupo_b]

        self.colisiones.append((grupo_a, grupo_b, funcion_a_llamar))

    def obtener_colisiones(self, actor, grupo_de_actores):
        "Retorna una lista de los actores que colisionan con uno en particular."

        lista_de_colisiones = []

        for a in grupo_de_actores:
            if id(actor) != id(a) and utils.colisionan(actor, a):
                lista_de_colisiones.append(a)

        return lista_de_colisiones
