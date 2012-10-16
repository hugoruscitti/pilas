# -*- encoding: utf-8 -*-
import pilas
import os
import random

from pilas.actores.actor import Actor
pilas.iniciar()


class Bala(Actor):
    def __init__(self, x, y):
        Actor.__init__(self,os.path.abspath("bala.png"), x, y)

pilas.fondos.Pasto()
arma = pilas.actores.Actor(os.path.abspath("arma.png"))
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40
tiempo = 6

enemigos = []

fin_de_juego = False


def crear_enemigo():

    enemigo = pilas.actores.Mono()
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)

    # Hace que la aceituna aparezca gradualmente, aumentando de tamaño.
    enemigo.escala = 0
    enemigo.escala = pilas.interpolar(0.5, duracion=0.5, tipo='rebote_final')

    enemigo.aprender(pilas.habilidades.PuedeExplotar)

    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180

    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180

    enemigo.x = x
    enemigo.y = y

    enemigos.append(enemigo)

    tipo_interpolacion = ['lineal',
                          'aceleracion_gradual',
                          'desaceleracion_gradual',
                          'rebote_inicial',
                          'rebote_final']

    enemigo.x = pilas.interpolar(0, tiempo, tipo=random.choice(tipo_interpolacion))
    enemigo.y = pilas.interpolar(0, tiempo, tipo=random.choice(tipo_interpolacion))

    if fin_de_juego:
        return False
    else:
        return True


def reducir_tiempo():
    global tiempo
    
    tiempo -= 1
    pilas.avisar("HURRY UP!!!")
    if tiempo < 1:
        tiempo = 0.5
    return True


def destruido(disparo, enemigo): 
    enemigo.eliminar()
    puntos.escala = 0
    puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
    puntos.aumentar(1)


def perder(arma, enemigo):

    enemigo.sonreir()
    arma.eliminar()
    pilas.escena_actual().tareas.eliminar_todas()
    fin_de_juego = True
    pilas.avisar("HAS PERDIDO. Conseguiste %d putnos" %(puntos.obtener()))

arma.aprender(pilas.habilidades.RotarConMouse,
              lado_seguimiento=pilas.habilidades.RotarConMouse.ARRIBA)


arma.aprender(pilas.habilidades.Disparar,
               actor_disparado=Bala,
               grupo_enemigos=enemigos,               
               cuando_elimina_enemigo=destruido,
               frecuencia_de_disparo=5,
               salida_disparo=pilas.habilidades.Disparar.ARRIBA,
               offset_disparo=27)

pilas.mundo.agregar_tarea(1, crear_enemigo)

pilas.mundo.agregar_tarea(20, reducir_tiempo)

pilas.escena_actual().colisiones.agregar(arma, enemigos, perder)

pilas.avisar("Pulsa ESPACIO y mueve el raton para matarlos.")
pilas.ejecutar()
