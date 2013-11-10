# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


from pilas import control
from pilas import fisica
from pilas.escena import Gestor, Normal
from pilas import dev


class Mundo(object):
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, motor, ancho, alto, titulo, rendimiento=60, area_fisica=None,
                 gravedad=(0, -10), pantalla_completa=False, centrado=True):

        self.gestor_escenas = Gestor()

        self.motor = motor
        self.motor.iniciar_ventana(ancho, alto, titulo, pantalla_completa, self.gestor_escenas, rendimiento, centrado)

        self.area_fisica = area_fisica
        self.gravedad = gravedad

    def crear_motor_fisica(self):
        if self.area_fisica != None:
            return fisica.crear_motor_fisica(self.area_fisica, gravedad=self.gravedad)
        else:
            return fisica.crear_motor_fisica(self.obtener_area(), gravedad=self.gravedad)

    def reiniciar(self):
        self.gestor_escenas.limpiar()
        self.gestor_escenas.cambiar_escena(Normal())
        self.motor.canvas.depurador.reiniciar()

    def terminar(self):
        self.motor.terminar()

    def ejecutar_bucle_principal(self):
        "Mantiene en funcionamiento el motor completo."
        self.motor.ejecutar_bucle_principal()

    def agregar_tarea_una_vez(self, time_out, function, *params):
        return self.gestor_escenas.escena_actual().tareas.una_vez(time_out, function, params)

    def agregar_tarea_siempre(self, time_out, function, *params):
        return self.gestor_escenas.escena_actual().tareas.siempre(time_out, function, params)

    def agregar_tarea(self, time_out, funcion, *parametros):
        return self.gestor_escenas.escena_actual().tareas.condicional(time_out, funcion, parametros)

    def deshabilitar_sonido(self, estado=True):
        self.motor.deshabilitar_sonido(estado)

    def deshabilitar_musica(self, estado=True):
        self.motor.deshabilitar_musica(estado)

    def definir_gravedad(self, x, y):
        """Define la gravedad del motor de física.

        :param x: Aceleración horizontal.
        :param y: Aceleración vertical.
        """
        self.gestor_escenas.escena_actual().fisica.definir_gravedad(x, y)

    def obtener_area(self):
        return (self.motor.ancho_original, self.motor.alto_original)

    @property
    @dev.deprecated(se_desactiva_en="0.79", se_elimina_en="0.8",
                    reemplazo="pilas.utils.agregar_tarea, agregar_tarea_una_vez o agregar_tarea_siempre")
    def tareas(self):
        return self.gestor_escenas.escena_actual().tareas

    @property
    @dev.deprecated(se_desactiva_en="0.79", se_elimina_en="0.8",
                    reemplazo="pilas.escena_actual().camara")
    def camara(self):
        return self.gestor_escenas.escena_actual().camara

    @property
    def colisiones(self):
        return self.gestor_escenas.escena_actual().colisiones

    @property
    def control(self):
        return self.gestor_escenas.escena_actual().control
