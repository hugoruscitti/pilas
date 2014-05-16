# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import camara
from pilasengine.actores import grupo
from pilasengine.utils import pitweener
from pilasengine.tareas import Tareas
from pilasengine.fisica import Fisica

class Escena(object):

    def __init__(self, pilas):
        self.pilas = pilas
        pilas.log("Creando una escena: ", self)
        self.camara = camara.Camara(pilas, self)
        self.tweener = pitweener.Tweener()
        self._actores = grupo.Grupo(pilas)
        self.grupos = []

        self.mueve_mouse = self.pilas.eventos.Evento('mueve_mouse')         # ['x', 'y', 'dx', 'dy']
        self.click_de_mouse = self.pilas.eventos.Evento('click_de_mouse')   # ['boton', 'x', 'y']
        self.termina_click = self.pilas.eventos.Evento('termina_click')     # ['boton', 'x', 'y']
        self.mueve_rueda = self.pilas.eventos.Evento('mueve_rueda')         # ['delta']
        self.pulsa_tecla = self.pilas.eventos.Evento('pulsa_tecla')         # ['codigo', 'texto']
        self.suelta_tecla = self.pilas.eventos.Evento('suelta_tecla')       # ['codigo', 'texto']
        self.pulsa_tecla_escape = self.pilas.eventos.Evento('pulsa_tecla_escape') #['']

        self.control = self.pilas.control.Control(self)
        self.tareas = Tareas(self)
        self.fisica = Fisica(self)

    def iniciar(self):
        pass

    def actualizar(self):
        pass

    def terminar(self):
        pass

    def actualizar_interpolaciones(self, tiempo_desde_ultima_actualizacion=None):
        self.tweener.update(tiempo_desde_ultima_actualizacion)

    def actualizar_actores(self):
        for x in self._actores.obtener_actores():
            x.pre_actualizar()
            x.actualizar()

    def dibujar_actores(self, painter):
        painter.save()

        self.camara.aplicar_transformaciones_completas(painter)

        for x in self._actores.obtener_actores(fijos=False, sin_padre=True):
            x.dibujar(painter)

        painter.restore()

        painter.save()
        self.camara.aplicar_translacion(painter)

        for x in self._actores.obtener_actores(fijos=True, sin_padre=True):
            x.dibujar(painter)

        painter.restore()

    def agregar_actor(self, actor):
        self._actores.agregar(actor)

    def agregar_grupo(self, grupo):
        self.grupos.append(grupo)