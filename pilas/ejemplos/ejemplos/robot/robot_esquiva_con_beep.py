# -*- encoding: utf-8 -*-

import pilas
from pilas.actores import Actor
from pilas.actores import Fantasma
from pilas.actores import Aceituna


def incrementarEscala(actores, escala):
    for f in  actores:
        f.escala = escala
    
def esquiva(robot):
    robot.backward(40, 1)
    robot.turnRight(50, 0.5)
    robot.forward()

pilas.iniciar()

fan = pilas.actores.Fantasma() * 8
aceitunas = pilas.actores.Aceituna() * 8

incrementarEscala(fan, 3)
incrementarEscala(aceitunas, 2)

b = pilas.actores.Board("/dev/tty/USB0")
robot = pilas.actores.Robot(b, 1)
robot.subelapiz()
robot.x = - 30
robot.y = -50

obstaculos = 0
esquiva(robot)

# Esquiva 10 obstáculos
robot.beep(2000,2)
while obstaculos < 10:
    if robot.getObstacle(15):
        robot.beep(2000,1)
        esquiva(robot)
        robot.forward()
        obstaculos = obstaculos + 1
robot.beep(2000,2)

robot.stop()

pilas.ejecutar()
