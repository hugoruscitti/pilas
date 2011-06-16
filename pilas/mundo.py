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


class Mundo:
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, motor, ancho, alto, titulo, fps=60, economico=True, gravedad=(0, -90)):
        self.motor = motor
        self.motor.iniciar_ventana(ancho, alto, titulo)

        self.tweener = pytweener.Tweener()
        self.tareas = tareas.Tareas() 
        self.control = control.Control()
        eventos.actualizar.conectar(self.actualizar_simuladores)

    def actualizar_simuladores(self, evento):
        self.tweener.update(16)
        self.tareas.actualizar(1/60.0)

    def terminar(self):
        pass

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."
        self.motor.ejecutar_bucle_principal(self, ignorar_errores)

'''

class __deprecated_Mundo():

        #self.fisica.actualizar()
        self.ventana = ventana.iniciar(ancho, alto, titulo)
        self.fps = fps
        self.economico = economico
        ventana.ancho = ancho
        ventana.alto = alto


        self.fps = pilas.fps.FPS(self.fps, self.economico)
        self.camara = camara.Camara(self.ventana)
        
        self.depurador = depurador.Depurador(self.fps)

        self.escena_actual = None

        # Genera los administradores de tareas e interpolaciones.
        
        # Genera el motor de fisica.
        self.fisica = pilas.fisica.Fisica(gravedad=gravedad)
        
        self.pausa_habilitada = False
        self.depuracion_fisica_habilitada = False
        self.funciones_depuracion = []
        self.salir = False


    def _realizar_actualizacion_logica(self, ignorar_errores):
        self.actualizar_simuladores()

        # Emite el aviso de actualizacion a los receptores.
        self.emitir_evento_actualizar()

        # Analiza colisiones entre los actores
        if ignorar_errores:
            try:
                self.analizar_colisiones()
            except Exception, e:
                print e
        else:
            self.analizar_colisiones()

        # Dibuja la escena actual y a los actores
        if ignorar_errores:
            try:
                self.escena_actual.actualizar()
            except Exception, e:
                print e
        else:
            self.escena_actual.actualizar()
        
        if ignorar_errores:
            try:
                self.actualizar_actores()
            except Exception, e:
                print e
        else:
            self.actualizar_actores()


    def cerrar_ventana(self):
        pilas.motor.cerrar_ventana()
        sys.exit(0)

    def definir_escena(self, escena_nueva):
        "Cambia la escena que se muestra en pantalla"
        self.escena_actual = escena_nueva
        escena_nueva.iniciar()

    def agregar_tarea_una_vez(self, time_out, function, *params): 
        self.tareas.una_vez(time_out, function, params)

    def agregar_tarea_siempre(self, time_out, function, *params): 
        self.tareas.siempre(time_out, function, params)

    def agregar_tarea(self, time_out, funcion, *parametros):
        self.tareas.condicional(time_out, funcion, parametros)

    def alternar_pausa(self):
        if self.pausa_habilitada:
            self.pausa_habilitada = False
            self.pausa.eliminar()
        else:
            self.pausa_habilitada = True
            self.pausa = pilas.actores.Actor("icono_pausa.png")
            self.pausa.z = -100
            

    def actualizar_actores(self):
        for actor in pilas.actores.todos:
            actor.actualizar()
            actor.actualizar_comportamientos()
            actor.actualizar_habilidades()

    def dibujar_actores(self):
        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        
        for actor in pilas.actores.todos:
            actor.dibujar(self.ventana)
            self.depurador.dibuja_actor(actor)

    def emitir_evento_actualizar(self):
        self.control.actualizar()
        pilas.eventos.actualizar.send("bucle")

    def analizar_colisiones(self):
        pilas.colisiones.verificar_colisiones()
'''
