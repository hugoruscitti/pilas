# -*- encoding: utf-8 -*-
import pilas
import os
import random

from pilas.actores.actor import Actor

pilas.iniciar()

def asignar_arma_simple():
    torreta.municion = municion_bala_simple

def asignar_arma_doble(estrella, disparo):
    torreta.municion = municion_doble_bala
    estrella.eliminar()
    pilas.mundo.agregar_tarea(10, asignar_arma_simple)
    pilas.avisar("ARMA MEJORADA")


def eliminar_estrella(estrella):
    estrella.eliminar()


def crear_enemigo():

    enemigo = pilas.actores.Mono()
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)

    # Hace que la aceituna aparezca gradualmente, aumentando de tamaño.
    enemigo.escala = 0
    enemigo.escala = pilas.interpolar(0.5, duracion=0.5, tipo='elastico_final')

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

    if random.randrange(0, 20) > 15:
        if issubclass(torreta.habilidades.DispararConClick.municion, municion_bala_simple):

            estrella = pilas.actores.Estrella(x,y)
            estrella.escala = pilas.interpolar(0.5, duracion=0.5, tipo='elastico_final')

            pilas.escena_actual().colisiones.agregar(estrella,
                                                     torreta.habilidades.DispararConClick.proyectiles,
                                                     asignar_arma_doble)

            pilas.mundo.agregar_tarea(3, eliminar_estrella, estrella)

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


def enemigo_destruido(disparo, enemigo):
    enemigo.eliminar()
    puntos.escala = 0
    puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
    puntos.aumentar(1)


def perder(torreta, enemigo):
    global fin_de_juego

    enemigo.sonreir()
    torreta.eliminar()
    pilas.escena_actual().tareas.eliminar_todas()
    fin_de_juego = True
    pilas.avisar("GAME OVER. Conseguiste %d puntos" %(puntos.obtener()))


pilas.fondos.Pasto()

puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40

tiempo = 6

enemigos = []

fin_de_juego = False

pilas.actores.Sonido()


municion_bala_simple = pilas.actores.Bala
municion_doble_bala = pilas.municion.BalasDoblesDesviadas

torreta = pilas.actores.Torreta(municion_bala_simple=municion_bala_simple,
                                enemigos=enemigos,
                                cuando_elimina_enemigo=enemigo_destruido)

pilas.mundo.agregar_tarea(1, crear_enemigo)

pilas.mundo.agregar_tarea(20, reducir_tiempo)

pilas.escena_actual().colisiones.agregar(torreta, enemigos, perder)

pilas.avisar("Pulsa pulsa y mueve el raton para destruirlos.")
pilas.ejecutar()
