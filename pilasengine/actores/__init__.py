# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import random

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
            raise Exception("Solo se pueden vincular clases que heredan de \
                            pilasengine.actores.Actor")

        def metodo_crear_actor(self):
            nuevo_actor = clase_del_actor(self.pilas)
            return nuevo_actor

        nombre_del_actor = clase_del_actor.__name__
        existe = getattr(self.__class__, nombre_del_actor, None)

        if existe:
            raise Exception("Lo siento, ya existe un actor con el nombre " +
                            nombre_del_actor)

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

            self.pilas.log("Agregando el actor", actor, "en la escena",
                           escena_actual)
            escena_actual.agregar_actor(actor)

            self.pilas.log("Iniciando el actor, llamando a actor.iniciar() \
                           del objeto ", actor)
            actor.iniciar()
        else:
            raise Exception("Solo puedes agregar actores de esta forma.")

        return actor

    def agregar_grupo(self, grupo):
        if isinstance(grupo, Grupo):
            escena_actual = self.pilas.obtener_escena_actual()
            self.pilas.log("Agregando el grupo", grupo, "a la escena",
                           escena_actual)
            escena_actual.agregar_grupo(grupo)
        else:
            raise Exception("Solo puedes agregar grupos de esta forma.")

        return grupo

    def Aceituna(self, x=0, y=0):
        return self._crear_actor('aceituna', 'Aceituna', x=x, y=y)

    def Mono(self, x=0, y=0):
        return self._crear_actor('mono', 'Mono', x=x, y=y)

    def Actor(self, x=0, y=0):
        return self._crear_actor('actor', 'Actor', x=x, y=y)

    def Palo(self, x=0, y=0):
        return self._crear_actor('palo', 'Palo', x=x, y=y)

    def Ejes(self, x=0, y=0):
        return self._crear_actor('ejes', 'Ejes', x=x, y=y)

    def Puntaje(self, x=0, y=0):
        return self._crear_actor('puntaje', 'Puntaje', x=x, y=y)

    def Pingu(self, x=0, y=0):
        return self._crear_actor('pingu', 'Pingu', x=x, y=y)

    def Martian(self, x=0, y=0):
        return self._crear_actor('martian', 'Martian', x=x, y=y)

    def CursorMano(self, x=0, y=0):
        return self._crear_actor('cursor_mano', 'CursorMano', x=x, y=y)

    def CursorDisparo(self, x=0, y=0):
        return self._crear_actor('cursor_disparo', 'CursorDisparo', x=x, y=y)

    def EstrellaNinja(self, x=0, y=0):
        return self._crear_actor('estrella_ninja', 'EstrellaNinja', x=x, y=y)

    def _crear_actor(self, modulo, clase, *k, **kw):
        import importlib

        referencia_a_modulo = importlib.import_module('pilasengine.actores.'
                                                      + modulo)
        referencia_a_clase = getattr(referencia_a_modulo, clase)

        nuevo_actor = referencia_a_clase(self.pilas, *k, **kw)
        # Importante: cuando se inicializa el actor, el método __init__
        #             realiza una llamada a pilas.actores.agregar_actor
        #             para vincular el actor a la escena.
        return nuevo_actor

    def MensajeError(self, error, descripcion):
        return self._crear_actor('mensaje_error', 'MensajeError', error,
                                 descripcion)

    def Animacion(self, grilla, ciclica=False, x=0, y=0, velocidad=10):
        return self._crear_actor('animacion', 'Animacion', grilla=grilla,
                                 ciclica=ciclica, x=x, y=y, velocidad=velocidad)

    def Grupo(self):
        import grupo
        nuevo_grupo = grupo.Grupo(self.pilas)
        return self.agregar_grupo(nuevo_grupo)

    def Banana(self, x=0, y=0):
        return self._crear_actor('banana', 'Banana', x=x, y=y)

    def Bala(self, x=0, y=0, rotacion=0, velocidad_maxima=9,
             angulo_de_movimiento=90):
        return self._crear_actor('bala', 'Bala', x=x, y=y, rotacion=rotacion,
                                 velocidad_maxima=velocidad_maxima,
                                 angulo_de_movimiento=angulo_de_movimiento)

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

    def Ovni(self, x=0, y=0):
        return self._crear_actor('ovni', 'Ovni', x=x, y=y)

    def Nave(self, x=0, y=0):
        return self._crear_actor('nave', 'Nave', x=x, y=y)

    def NaveKids(self, x=0, y=0):
        return self._crear_actor('nave_kids', 'NaveKids', x=x, y=y)

    def Planeta(self, x=0, y=0):
        return self._crear_actor('planeta', 'Planeta', x=x, y=y)

    def Piedra(self, x=0, y=0):
        return self._crear_actor('piedra', 'Piedra', x=x, y=y)

    def Pelota(self, x=0, y=0):
        return self._crear_actor('pelota', 'Pelota', x=x, y=y)

    def Caja(self, x=0, y=0):
        return self._crear_actor('caja', 'Caja', x=x, y=y)

    def Zanahoria(self, x=0, y=0):
        return self._crear_actor('zanahoria', 'Zanahoria', x=x, y=y)

    def Cooperativista(self, x=0, y=0):
        return self._crear_actor('cooperativista', 'Cooperativista', x=x, y=y)

    def Pacman(self, x=0, y=0):
        return self._crear_actor('pacman', 'Pacman', x=x, y=y)

    def Globo(self, texto, x=0, y=0, dialogo=None, avance_con_clicks=True,
              autoeliminar=False, ancho_globo=0, alto_globo=0):
        return self._crear_actor('globo', 'Globo', texto=texto, x=x, y=y,
                                 dialogo=dialogo,
                                 avance_con_clicks=avance_con_clicks,
                                 autoeliminar=autoeliminar,
                                 ancho_globo=ancho_globo,
                                 alto_globo=alto_globo)

    def Texto(self, cadena_de_texto="Sin texto", magnitud=20, vertical=False,
              fuente=None, fijo=True, ancho=0, x=0, y=0):
        import texto
        nuevo_actor = texto.Texto(self.pilas, cadena_de_texto, magnitud,
                                  vertical, fuente, fijo, ancho)
        nuevo_actor.x = x
        nuevo_actor.y = y
        return nuevo_actor

    def TextoInferior(self, texto="Sin texto", magnitud=20, vertical=False,
                      fuente=None, fijo=True, ancho=0, x=0, y=0, retraso=5):
        import texto_inferior
        nuevo_actor = texto_inferior.TextoInferior(self.pilas, texto, magnitud,
                                                   vertical, fuente, fijo,
                                                   ancho, x=x, y=x,
                                                   retraso=retraso)
        return nuevo_actor

    def fabricar(self, clase, cantidad):
        grupo = self.Grupo()
        ancho_ventana, alto_ventana = self.pilas.widget.obtener_area()

        for i in xrange(cantidad):
            _x = random.randint(-ancho_ventana/2, ancho_ventana/2)
            _y = random.randint(-alto_ventana/2, alto_ventana/2)
            grupo.agregar(clase(self.pilas, x=_x, y=_y))

        return grupo