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
puntos = pilas.actores.Puntaje(x=250, y=200)

enemigos = []

fin_de_juego = False


def crear_enemigo():

    global enemigos
    global fin_de_juego

    enemigo = pilas.actores.Aceituna()
    x = random.randrange(-320,320)
    y = random.randrange(-240,240)

    print x
    print y

    if x < 100 and x > 0:
        x = 150 
    if x < -100 and x < 0:
        x = -150 

    if y < 100 and y > 0:
        y = 150 
    if y < -100 and y < 0:
        y = -150 

    enemigo.x = x
    enemigo.y = y
    
    enemigos.append(enemigo)

    tipo_interpolacion = ['lineal',
                          'aceleracion_gradual',
                          'desaceleracion_gradual',
                          'rebote_inicial',
                          'rebote_final']
    
    enemigo.x = pilas.interpolar(0,3, tipo=random.choice(tipo_interpolacion))
    enemigo.y = pilas.interpolar(0,3, tipo=random.choice(tipo_interpolacion))
    
    if fin_de_juego:
        return False
    else:
        return True


def destruido(disparo, enemigo):
    enemigo.eliminar()
    puntos.aumentar(1)


def perder(arma, enemigo):
    global fin_de_juego
    global enemigos

    arma.eliminar()
    fin_de_juego = True
    pilas.avisar("HAS PERDIDO")

arma.aprender(pilas.habilidades.RotarConMouse,
              lado_seguimiento=pilas.habilidades.RotarConMouse.ARRIBA)

arma.aprender(pilas.habilidades.Disparar,
               actor_disparado=Bala,
               grupo_enemigos=enemigos,
               cuando_elimina_enemigo=destruido,
               salida_disparo=pilas.habilidades.Disparar.ARRIBA)

pilas.mundo.agregar_tarea(1, crear_enemigo)

pilas.escena_actual().colisiones.agregar(arma, enemigos, perder)

pilas.avisar("Pulsa ESPACIO y mueve el raton para matarlos.")
pilas.ejecutar()
