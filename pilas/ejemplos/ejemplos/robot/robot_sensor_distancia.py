# -*- encoding: utf-8 -*-

import pilas
pilas.iniciar()



def evaluar(unRobot, unMono):

        def checkPosicion():
            print r.ping()

            if (r.ping() > 30) :       
                print r.ping()         
                return True
            else:
                # Si se acercó el mono le avisa
                m.decir("Cuidado!!!!!")                
                r.stop() 
                return False

        r.forward()

        pilas.escena_actual().tareas.condicional(0.5, checkPosicion)


b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b, 1)
m = pilas.actores.Mono()


r.x = 11
r.y = -30
m.x = 15
m.y = 140

evaluar(r, m)

pilas.ejecutar()
