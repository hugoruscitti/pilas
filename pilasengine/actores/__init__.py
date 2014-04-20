# -*- encoding: utf-8 -*-

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
        escena_actual = self.pilas.obtener_escena_actual()

        self.pilas.log("Agregando el actor", actor, "en la escena", escena_actual)
        escena_actual.agregar_actor(actor)

        self.pilas.log("Iniciando el actor, llamando a actor.iniciar() del objeto ", actor)
        actor.iniciar()

        return actor

    def agregar_grupo(self, grupo):
        escena_actual = self.pilas.obtener_escena_actual()

        self.pilas.log("Agregando el grupo", grupo, "a la escena", escena_actual)
        escena_actual.agregar_grupo(grupo)

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

    def Grupo(self):
        import grupo
        nuevo_grupo = grupo.Grupo(self.pilas)
        return self.agregar_grupo(nuevo_grupo)