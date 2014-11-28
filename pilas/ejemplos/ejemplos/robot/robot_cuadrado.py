# -*- encoding: utf-8 -*-
import pilas

def cuadrado(robot):
    robot.forward(100,2)
    robot.turnLeft(100,1.6)

pilas.iniciar()
b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b, 1)

pilas.avisar("El Robor hace un cuadrado.")

for i in range(0,4):
    cuadrado(r)

pilas.ejecutar()
