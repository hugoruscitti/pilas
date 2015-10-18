# -*- encoding: utf-8 -*-
import pilasengine
import os
import random

from pilasengine.actores.actor import Actor

pilas = pilasengine.iniciar()

def asignar_arma_simple():
    torreta.municion = municion_bala_simple

def asignar_arma_doble(estrella, disparo):
    torreta.municion = municion_doble_bala
    estrella.eliminar()
    pilas.tareas.siempre(10, asignar_arma_simple)
    pilas.avisar("ARMA MEJORADA")


def eliminar_estrella(estrella):
    estrella.eliminar()


def crear_enemigo():

    enemigo = pilas.actores.Mono()
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)

    # Hace que la aceituna aparezca gradualmente, aumentando de tamaño.
    enemigo.escala = 0
    pilas.utils.interpolar(enemigo, 'escala', 0.5, duracion=0.5, tipo='elastico')

    enemigo.aprender("PuedeExplotar")

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

    tipo_interpolacion = ["lineal",
                          "aceleracion_gradual",
                          "desaceleracion_gradual",
                          "gradual"]

    interpolacion = random.choice(tipo_interpolacion)

    pilas.utils.interpolar(enemigo, 'x', 0, duracion=tiempo, tipo=interpolacion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion=tiempo, tipo=interpolacion)

    if random.randrange(0, 20) > 15:
        if issubclass(torreta.habilidades.DispararConClick.municion, municion_bala_simple):

            estrella = pilas.actores.Estrella(x,y)
            pilas.utils.interpolar(estrella, 'escala', 0.5, duracion=0.5, tipo='elastico')

            pilas.colisiones.agregar(estrella,
                                     torreta.habilidades.DispararConClick.proyectiles,
                                     asignar_arma_doble)

            pilas.tareas.siempre(3, eliminar_estrella, estrella)

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
    pilas.utils.interpolar(puntos, 'escala', 1, duracion=0.5, tipo='elastico')
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


municion_bala_simple = pilasengine.actores.Bala
municion_doble_bala = pilasengine.actores.BalasDoblesDesviadas

torreta = pilas.actores.Torreta(municion_bala_simple=municion_bala_simple,
                                enemigos=enemigos,
                                cuando_elimina_enemigo=enemigo_destruido)

pilas.tareas.siempre(1, crear_enemigo)

pilas.tareas.siempre(20, reducir_tiempo)

pilas.colisiones.agregar(torreta, enemigos, perder)

pilas.avisar("Pulsa pulsa y mueve el raton para destruirlos.")
pilas.ejecutar()
