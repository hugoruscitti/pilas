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
    _lista_actores_personalizados = []

    def __init__(self, pilas):
        self.pilas = pilas

    def vincular(self, clase_del_actor):
        """Permite vincular una clase de actor con pilas.

        Esto permite de después el actor se pueda crear desde
        el módulo "pilas.actores".

        Por ejemplo, si tengo una clase ``MiActor`` lo puedo
        vincular con:

            >>> pilas.actores.vincular(MiActor)
            >>> mi_actor = pilas.actores.MiActor()

        """

        if not Actor in clase_del_actor.__bases__:
            raise Exception("Solo se pueden vincular clases que heredan de pilasengine.actores.Actor")

        def metodo_crear_actor(self):
            nuevo_actor = clase_del_actor(self.pilas)
            return nuevo_actor

        nombre_del_actor = clase_del_actor.__name__
        existe = getattr(self.__class__, nombre_del_actor, None)

        if existe:
            raise Exception("Lo siento, ya existe un actor con el nombre " + nombre_del_actor)

        setattr(self.__class__, nombre_del_actor, metodo_crear_actor)
        Actores._lista_actores_personalizados.append(nombre_del_actor)

    def obtener_actores_personalizados(self):
        "Retorna una lista con todos los nombres de actores personalizados."
        return Actores._lista_actores_personalizados

    def eliminar_actores_personalizados(self):
        "Recorre todos los actores personalizados y los elimina."
        for x in Actores._lista_actores_personalizados:
            delattr(self.__class__, x)

        Actores._lista_actores_personalizados = []

    def agregar_actor(self, actor):
        """Agrega un actor a la escena actual.

        Este método se ejecuta internamente cada vez que se
        contruye un actor escribiendo algo como:

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
        return self._crear_actor('aceituna', 'Aceituna')

    def Mono(self):
        return self._crear_actor('mono', 'Mono')

    def Actor(self):
        return self._crear_actor('actor', 'Actor')

    def Palo(self):
        return self._crear_actor('palo', 'Palo')

    def _crear_actor(self, modulo, clase, *k, **kw):
        import importlib

        referencia_a_modulo = importlib.import_module('pilasengine.actores.' + modulo)
        referencia_a_clase = getattr(referencia_a_modulo, clase)

        nuevo_actor = referencia_a_clase(self.pilas, *k, **kw)
        # Importante: cuando se inicializa el actor, el método __init__
        #             realiza una llamada a pilas.actores.agregar_actor
        #             para vincular el actor a la escena.
        return nuevo_actor

    def MensajeError(self, error):
        return self._crear_actor('mensaje_error', 'MensajeError')

    def Animacion(self, grilla, ciclica=False, x=0, y=0, velocidad=10):
        return self._crear_actor('animacion', 'Animacion', grilla=grilla, ciclica=ciclica, x=x, y=y, velocidad=velocidad)

    def Grupo(self):
        import grupo
        nuevo_grupo = grupo.Grupo(self.pilas)
        return self.agregar_grupo(nuevo_grupo)

    def Banana(self, x=0, y=0):
        return self._crear_actor('banana', 'Banana', x=x, y=y)

    def Bomba(self, x=0, y=0):
        return self._crear_actor('bomba', 'Bomba', x=x, y=y)

    def Explosion(self, x=0, y=0):
        return self._crear_actor('explosion', 'Explosion', x=x, y=y)

    def Estrella(self, x=0, y=0):
        return self._crear_actor('estrella', 'Estrella', x=x, y=y)

    def Fantasma(self, x=0, y=0):
        return self._crear_actor('fantasma', 'Fantasma', x=x, y=y)

    def Manzana(self, x=0, y=0):
        return self._crear_actor('manzana', 'Manzana', x=x, y=y)

    def Texto(self, cadena_de_texto="Sin texto", magnitud=20, vertical=False,
              fuente=None, fijo=True, ancho=0, x=0, y=0):
        import texto
        nuevo_actor = texto.Texto(self.pilas, cadena_de_texto, magnitud, vertical,
                                  fuente, fijo, ancho)
        nuevo_actor.x = x
        nuevo_actor.y = y
        return nuevo_actor