# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

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
        self._colisiones_en_curso = []
        self._lista = []

    def notificar_colision(self, fixture_1, fixture_2):
        """Se invoca automáticamente desde el componente Fisica.

        Internamente, el motor de física tiene un objeto llamado
        ContactListener (en el archivo 'fisica/contact_listener.py').
        """
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)

        info_colision = {'actor1': actor_asociado_1,
                         'actor2': actor_asociado_2}

        if actor_asociado_1 and actor_asociado_2:
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
                            funcion_a_llamar(a, b)

    def agregar(self, grupo_a, grupo_b, funcion_a_llamar):
        "Agrega dos listas de actores para analizar _colisiones."

        if not isinstance(grupo_a, list):
            grupo_a = [grupo_a]

        if not isinstance(grupo_b, list):
            grupo_b = [grupo_b]

        self._colisiones_programadas_con_respuesta.append((grupo_a, grupo_b, funcion_a_llamar))

    """
    def verificar_colisiones(self):
        print self._colisiones

        # Analiza las colisiones físicas reportadas por box2d.
        for info_colision in []:
            actor_1 = info_colision['actor_1']
            actor_2 = info_colision['actor_2']

            # Luego recorre la lista de colisiones programadas, en busca
            # de cualquier callback asociada a los dos actores que entraron
            # en contacto.
            for (grupo_a, grupo_b, funcion_a_llamar) in self._colisiones:

                for a in grupo_a:
                    for b in grupo_b:

                        if a in (actor_1, actor_2) and b in (actor_1, actor_2):
                            print "ASDASD"
                            #funcion_a_llamar(a, b)

        #self._colisiones_actuales = []


        #for x in self._colisiones:
        #    self._verificar_colisiones_en_tupla(x)
        """

    """
    def _verificar_colisiones_en_tupla(self, tupla):
        "Toma dos grupos de actores y analiza _colisiones entre ellos."
        (grupo_a, grupo_b, funcion_a_llamar) = tupla

        for a in grupo_a:
            for b in grupo_b:
                try:
                    if id(a) != id(b) and utils.colisionan(a, b):
                        funcion_a_llamar(a, b)

                    # verifica si alguno de los dos objetos muere en la colision.
                    if a not in self.pilas.escena_actual().actores:
                        if a in grupo_a:
                            list.remove(grupo_a, a)

                    if b not in self.pilas.escena_actual().actores:
                        if b in grupo_b:
                            list.remove(grupo_b, b)
                except Exception as e:
                    list.remove(grupo_a, a)
                    raise e

    def verificar_colisiones_fisicas(self, id_actor_a, id_actor_b):
        for x in self._colisiones:
            self._verificar_colisiones_fisicas_en_tupla(x, id_actor_a, id_actor_b)

    def _verificar_colisiones_fisicas_en_tupla(self, tupla, id_actor_a, id_actor_b):
        "Toma dos grupos de actores y analiza _colisiones entre ellos."
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
    """


    """
    def eliminar_colisiones_con_actor(self, actor):

        for x in self._colisiones:

            grupo_a = x[0]
            grupo_b = x[1]
            #funcion_a_llamar = x[2]

            if actor in grupo_a:
                # Si solo estaba el actor en este grupo eliminamos la colision.
                if len(grupo_a) == 1:
                    self._colisiones.remove(x)
                else:
                    # Si hay mas de un actore eliminamos el actor de la lista.
                    grupo_a.remove(x)
                break

            if actor in grupo_b:
                # Si solo estaba el actor en este grupo eliminamos la colision.
                if len(grupo_b) == 1:
                    self._colisiones.remove(x)
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

    """