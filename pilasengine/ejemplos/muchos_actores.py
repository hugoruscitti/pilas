import sys

import pilasengine
import random

pilas = pilasengine.iniciar()


def crear_actor():
    actor = pilas.actores.Actor()
    actor.imagen = "conejo.png"
    actor.rotacion = [360], 20
    actor.x = random.randint(-300, 300)
    actor.y = random.randint(-200, 200)
    actor.escala = 1 + (random.randint(-5, 5)) / 10.0
    return actor

for x in range(5):
    crear_actor()

pilas.camara.rotacion = [360], 20
pilas.camara.aumento = [2], 20
pilas.ejecutar()
