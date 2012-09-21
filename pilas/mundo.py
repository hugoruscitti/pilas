# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from pilas import actores, camara, colisiones, control, escenas, eventos, fisica, \
    tareas
from pilas.escena import gestor, escena_normal
import pytweener



class Mundo(object):
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, motor, ancho, alto, titulo, fps=60, gravedad=(0, -10), pantalla_completa=False):
        
        self.gestor_escenas = gestor.Gestor()        
        
        self.motor = motor
        self.motor.iniciar_ventana(ancho, alto, titulo, pantalla_completa, self.gestor_escenas)

        self.tweener = pytweener.Tweener()
        #self.tareas = tareas.Tareas()
        self.control = control.Control()
        self.colisiones = colisiones.Colisiones()
        self.camara = camara.Camara(self)

        eventos.actualizar.conectar(self.actualizar_simuladores)
        self.fisica = fisica.crear_motor_fisica(motor.obtener_area(), gravedad=gravedad)
        
    def reiniciar(self):
        self.gestor_escenas.limpiar()
        self.gestor_escenas.cambiar_escena(escena_normal.EscenaNormal())
        #self.tareas.eliminar_todas()
        self.tweener.eliminar_todas()
        #self.fisica.reiniciar()

    def actualizar_simuladores(self, evento):
        self.tweener.update(16)
        #self.tareas.actualizar(1/60.0)
        if self.fisica:
            self.fisica.actualizar()
        self.colisiones.verificar_colisiones()

    def terminar(self):
        self.motor.terminar()

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."
        self.motor.ejecutar_bucle_principal(self, ignorar_errores)

    def agregar_tarea_una_vez(self, time_out, function, *params):
        return self.tareas.una_vez(time_out, function, params)

    def agregar_tarea_siempre(self, time_out, function, *params):
        return self.tareas.siempre(time_out, function, params)

    def agregar_tarea(self, time_out, funcion, *parametros):
        return self.tareas.condicional(time_out, funcion, parametros)

    def deshabilitar_sonido(self, estado=True):
        self.motor.deshabilitar_sonido(estado)

    def deshabilitar_musica(self, estado=True):
        self.motor.deshabilitar_musica(estado)
