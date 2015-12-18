# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import camara
import pilasengine
from pilasengine.actores import grupo
from pilasengine.utils import pitweener
from pilasengine.tareas import Tareas
from pilasengine.fisica import Fisica
from pilasengine.colisiones import Colisiones

class Escena(object):

    def __init__(self, pilas):
        if not pilas:
            mensaje = "Ten cuidado, tienes que enviar 'pilas' como argumento de la escena al crearla."
            raise Exception(mensaje)

        if not isinstance(pilas, pilasengine.Pilas):
            mensaje = "Tienes que enviar el objeto 'pilas' como argumento a la escena al crearla, en lugar de eso llego esto: " + str(pilas)
            raise Exception(mensaje)

        self.pilas = pilas

        nombre_de_la_escena = self.__class__.__name__

        if not self.pilas.escenas.es_escena_vinculada(nombre_de_la_escena):
            raise Exception("La escena %s no ha sido vinculada. Ejecuta con pilas.escenas.vincular(%s) antes." %(nombre_de_la_escena, nombre_de_la_escena))

        pilas.log("Creando una escena: ", self)
        self.camara = camara.Camara(pilas, self)
        self.tweener = pitweener.Tweener()
        self._actores = grupo.Grupo(pilas)
        self.grupos = []

        self.mueve_camara = self.pilas.eventos.Evento('mueve_camara')       # ['x', 'y', 'dx', 'dy']
        self.mueve_mouse = self.pilas.eventos.Evento('mueve_mouse')         # ['x', 'y', 'dx', 'dy']
        self.click_de_mouse = self.pilas.eventos.Evento('click_de_mouse')   # ['boton', 'x', 'y']
        self.termina_click = self.pilas.eventos.Evento('termina_click')     # ['boton', 'x', 'y']
        self.mueve_rueda = self.pilas.eventos.Evento('mueve_rueda')         # ['delta']
        self.pulsa_tecla = self.pilas.eventos.Evento('pulsa_tecla')         # ['codigo', 'texto']
        self.suelta_tecla = self.pilas.eventos.Evento('suelta_tecla')       # ['codigo', 'texto']
        self.pulsa_tecla_escape = self.pilas.eventos.Evento('pulsa_tecla_escape') #['']
        self.cuando_actualiza = self.pilas.eventos.Evento('actualizar')     #['']
        self.pulsa_boton = self.pilas.eventos.Evento('pulsa_boton')         #['numero']
        self.mueve_pad = self.pilas.eventos.Evento('mueve_pad')         #['x', 'y', 'x1', 'y1']

        self.control = self.pilas.controles.Control(self)
        self.tareas = Tareas(self, pilas)
        self.fisica = Fisica(self, pilas)
        self.fisica.iniciar()
        self.colisiones = Colisiones(pilas, self)

        self.click_de_mouse.conectar(self.arrastrar_actor_mas_cercano)

    def eliminar_el_motor_de_fisica(self):
        """Método especial que se invoca cuando se reinicia pilas, y se tiene que eliminar la escena actual."""
        self.fisica.eliminar_para_liberar_memoria()

    def iniciar(self):
        pass

    def actualizar(self):
        pass

    def terminar(self):
        pass

    def actualizar_fisica(self):
        self.fisica.actualizar()

    def actualizar_interpolaciones(self, tiempo_desde_ultima_actualizacion=None):
        self.tweener.update(tiempo_desde_ultima_actualizacion)

    def actualizar_interpolaciones_en_modo_pause(self):
        self.tweener.update_time_without_motion()

    def forzar_actualizacion_de_interpolaciones(self):
        self.tweener.force_update_one_frame()

    def obtener_cantidad_de_actores(self):
        return len(self._actores.obtener_actores())

    def actualizar_actores(self):
        actores_a_eliminar = []
        self.pilas.pad.actualizar()

        for x in self._actores.obtener_actores():
            if x._vivo:
                x.pre_actualizar()
                x.actualizar()
                x.pos_actualizar()
            else:
                actores_a_eliminar.append(x)

        for actor in actores_a_eliminar:
            actor.quitar_de_la_escena_completamente()

    def dibujar_actores(self, painter):
        painter.save()

        self.camara.aplicar_transformaciones_completas(painter)

        for x in self._actores.obtener_actores(fijos=False, sin_padre=True):
            if x._vivo:
                x.dibujar(painter)

        painter.restore()

        painter.save()
        self.camara.aplicar_translacion(painter)

        for x in self._actores.obtener_actores(fijos=True, sin_padre=True):
            if x._vivo:
                x.dibujar(painter)

        painter.restore()

    def agregar_actor(self, actor):
        self._actores.agregar(actor)

    def agregar_grupo(self, grupo):
        self.grupos.append(grupo)

    def obtener_actores_en(self, x, y):
        return [a for a in self._actores.obtener_actores()
                if a.colisiona_con_un_punto(x, y)]

    def arrastrar_actor_mas_cercano(self, evento):
        actores_debajo_de_mouse = self.obtener_actores_en(evento.x, evento.y)

        if actores_debajo_de_mouse:
            actores_debajo_de_mouse = actores_debajo_de_mouse[::-1]

            for actor_cercano in actores_debajo_de_mouse:
                if actor_cercano.tiene_habilidad(self.pilas.habilidades.Arrastrable):
                    actor_cercano.habilidades.Arrastrable.intentar_arrastrar()
                    return True
