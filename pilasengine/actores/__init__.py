# -*- encoding: utf-8 -*-
from pilasengine.actores.actor import Actor
from pilasengine.actores.grupo import Grupo

class Actores(object):
    """Representa la forma de acceso y construcción de actores.

    Esta clase representa el objeto creado por pilas que
    se puede acceder escribiendo ``pilas.actores``. Desde aquí
    se puede acceder a los actores pre-diseñados de pilas y
    agregarlos a la escena.

    Por ejemplo, para crear una nave en pantalla podemos escribir:

        >>> nave = pilas.actores.Nave()

    """

    def __init__(self, pilas):
        self.pilas = pilas

    def agregar_actor(self, actor):
        """Agrega un actor a la escena actual.

        Este método se ejecuta internamente cada vez que se
        contruye un actor escribiendo algo cómo:

            >>> actor = pilas.actores.Actor()
        """
        if isinstance(actor, Actor):
            escena_actual = self.pilas.obtener_escena_actual()

            self.pilas.log("Agregando el actor", actor, "en la escena", escena_actual)
            escena_actual.agregar_actor(actor)

            self.pilas.log("Iniciando el actor, llamando a actor.iniciar() del objeto ", actor)
            actor.iniciar()
        else:
            raise Exception("Solo puedes agregar actores de esta forma.")

        return actor

    def agregar_grupo(self, grupo):
        if isinstance(grupo, Grupo):
            escena_actual = self.pilas.obtener_escena_actual()
            self.pilas.log("Agregando el grupo", grupo, "a la escena", escena_actual)
            escena_actual.agregar_grupo(grupo)
        else:
            raise Exception("Solo puedes agregar grupos de esta forma.")

        return grupo

    def Aceituna(self):
        import aceituna
        nuevo_actor = aceituna.Aceituna(self.pilas)
        return self.agregar_actor(nuevo_actor)

    def Mono(self):
        import mono
        nuevo_actor = mono.Mono(self.pilas)
        return self.agregar_actor(nuevo_actor)

    def Actor(self):
        import actor
        nuevo_actor = actor.Actor(self.pilas)
        return self.agregar_actor(nuevo_actor)

    def Palo(self):
        return self._crear_actor('palo', 'Palo')

    def _crear_actor(self, modulo, clase):
        import importlib

        referencia_a_modulo = importlib.import_module('pilasengine.actores.' + modulo)
        referencia_a_clase = getattr(referencia_a_modulo, clase)

        nuevo_actor = referencia_a_clase(self.pilas)
        return self.agregar_actor(nuevo_actor)


    def MensajeError(self, error):
        import mensaje_error
        nuevo_actor = mensaje_error.MensajeError(self.pilas, error)
        return self.agregar_actor(nuevo_actor)

    def Grupo(self):
        import grupo
        nuevo_grupo = grupo.Grupo(self.pilas)
        return self.agregar_grupo(nuevo_grupo)

    def Texto(self, cadena_de_texto="Sin texto", magnitud=20, vertical=False,
              fuente=None, fijo=True, ancho=0, x=0, y=0):
        import texto
        nuevo_actor = texto.Texto(self.pilas, cadena_de_texto, magnitud, vertical,
                                  fuente, fijo, ancho)
        nuevo_actor.x = x
        nuevo_actor.y = y
        return self.agregar_actor(nuevo_actor)