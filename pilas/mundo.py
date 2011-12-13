# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pytweener
from pilas import eventos
from pilas import tareas
from pilas import control
from pilas import fisica
from pilas import escenas
from pilas import colisiones
from pilas import camara
from pilas import actores


class Mundo(object):
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, motor, ancho, alto, titulo, fps=60, economico=True, 
            gravedad=(0, -90), pantalla_completa=False):
        self.motor = motor
        self.motor.iniciar_ventana(ancho, alto, titulo, pantalla_completa)

        self.tweener = pytweener.Tweener()
        self.tareas = tareas.Tareas() 
        self.control = control.Control()
        self.colisiones = colisiones.Colisiones()
        self.camara = camara.Camara(self)

        eventos.actualizar.conectar(self.actualizar_simuladores)
        eventos.actualizar_pausado.conectar(self.actualizar_simuladores_pausado)
        self.fisica = fisica.Fisica(motor.obtener_area(), gravedad=gravedad)
        self.escena_actual = None

    def reiniciar(self):
        self.fisica.reiniciar()

    def actualizar_simuladores(self, evento):
        self.tweener.update(16)
        self.tareas.actualizar(1/60.0)
        self.fisica.actualizar()
        self.colisiones.verificar_colisiones()

    def actualizar_simuladores_pausado(self, evento):
        self.tweener.update(0)
        self.tareas.actualizar(1/60.0)
        self.fisica.actualizar(velocidad=0)
        self.colisiones.verificar_colisiones()

    def terminar(self):
        self.motor.terminar()

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."
        self.motor.ejecutar_bucle_principal(self, ignorar_errores)

    def definir_escena(self, escena_nueva):
        "Cambia la escena que se muestra en pantalla"
        actores.utils.destruir_a_todos()
        self.tareas.eliminar_todas()

        if self.escena_actual:
            self.escena_actual.terminar()

        self.escena_actual = escena_nueva
        escena_nueva.iniciar()

    def agregar_tarea_una_vez(self, time_out, function, *params): 
        return self.tareas.una_vez(time_out, function, params)

    def agregar_tarea_siempre(self, time_out, function, *params): 
        return self.tareas.siempre(time_out, function, params)

    def agregar_tarea(self, time_out, funcion, *parametros):
        return self.tareas.condicional(time_out, funcion, parametros)
