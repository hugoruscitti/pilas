# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from . import utils
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
                    if a not in pilas.escena_actual().actores:
                        if a in grupo_a:
                            list.remove(grupo_a, a)

                    if b not in pilas.escena_actual().actores:
                        if b in grupo_b:
                            list.remove(grupo_b, b)
                except Exception as e:
                    list.remove(grupo_a, a)
                    raise e

    def verificar_colisiones_fisicas(self, id_actor_a, id_actor_b):
        for x in self.colisiones:
            self._verificar_colisiones_fisicas_en_tupla(x, id_actor_a, id_actor_b)

    def _verificar_colisiones_fisicas_en_tupla(self, tupla, id_actor_a, id_actor_b):
        "Toma dos grupos de actores y analiza colisiones entre ellos."
        (grupo_a, grupo_b, funcion_a_llamar) = tupla

        for a in grupo_a:
            for b in grupo_b:
                try:
                    if self._es_objeto_fisico_con_actor_asociado(a):
                        a_id = a.figura.id
                    else:
                        a_id = a.id

                    if self._es_objeto_fisico_con_actor_asociado(b):
                        b_id = b.figura.id
                    else:
                        b_id = b.id

                    if a_id == id_actor_a and b_id == id_actor_b:
                        funcion_a_llamar(a, b)

                        # verifica si alguno de los dos objetos muere en la colision.
                        if (self._es_objeto_fisico_con_actor_asociado(a)):
                            if a not in pilas.escena_actual().actores:
                                if a in grupo_a:
                                    list.remove(grupo_a, a)

                        if (self._es_objeto_fisico_con_actor_asociado(b)):
                            if b not in pilas.escena_actual().actores:
                                if b in grupo_b:
                                    list.remove(grupo_b, b)

                except Exception as e:
                    list.remove(grupo_a, a)
                    raise e


    def _es_objeto_fisico_con_actor_asociado(self, objeto):
        # Comprobamos si el objeto tiene la propiedad "figura" establecida.
        # Esta propiedad se establece en la Habilidad de Imitar.
        return hasattr(objeto, 'figura')

    def agregar(self, grupo_a, grupo_b, funcion_a_llamar):
        "Agrega dos listas de actores para analizar colisiones."

        if not isinstance(grupo_a, list):
            grupo_a = [grupo_a]

        if not isinstance(grupo_b, list):
            grupo_b = [grupo_b]

        self.colisiones.append((grupo_a, grupo_b, funcion_a_llamar))

    def eliminar_colisiones_con_actor(self, actor):

        for x in self.colisiones:

            grupo_a = x[0]
            grupo_b = x[1]
            #funcion_a_llamar = x[2]

            if actor in grupo_a:
                # Si solo estaba el actor en este grupo eliminamos la colision.
                if len(grupo_a) == 1:
                    self.colisiones.remove(x)
                else:
                    # Si hay mas de un actore eliminamos el actor de la lista.
                    grupo_a.remove(x)
                break

            if actor in grupo_b:
                # Si solo estaba el actor en este grupo eliminamos la colision.
                if len(grupo_b) == 1:
                    self.colisiones.remove(x)
                else:
                    # Si hay mas de un actore eliminamos el actor de la lista.
                    grupo_b.remove(x)
                break

    def obtener_colisiones(self, actor, grupo_de_actores):
        "Retorna una lista de los actores que colisionan con uno en particular."

        lista_de_colisiones = []

        for a in grupo_de_actores:
            if id(actor) != id(a) and utils.colisionan(actor, a):
                lista_de_colisiones.append(a)

        return lista_de_colisiones
