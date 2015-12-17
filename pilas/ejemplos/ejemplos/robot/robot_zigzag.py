# -*- encoding: utf-8 -*-
import pilas

def zigzag(robot):
    robot.turnRight(100,1.6)
    robot.forward(100,2)
    robot.turnLeft(100,1.6)
    robot.forward(100,2)


pilas.iniciar()
b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b,1)
r.subelapiz()
r.x = -300
r.y = 300 
r.bajalapiz()

pilas.avisar("El robot hace zigzag")

for i in range(0,6):
    zigzag(r)

pilas.ejecutar()
