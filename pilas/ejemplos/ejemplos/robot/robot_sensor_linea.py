import pilas
pilas.iniciar()



def decidir(unRobot):

        def checkPixel():
            iq, dr = r.getLine()
            print iq, dr

            if (iq != 255.0 and  dr != 255.0) :
                return True
            else:
                r.stop()
                return False

        r.forward()

        pilas.escena_actual().tareas.condicional(0.5, checkPixel)


b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b, 1)

pilas.fondos.FondoPersonalizado("robot_lineas.png")


r.y = -230
decidir(r)

pilas.ejecutar()
