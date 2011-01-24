# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
pilas.iniciar()

class layers:
    def __init__(self):
        self.capas = []
        pilas.mundo.agregar_tarea(0, self.actualizar_pantalla)


    
    def agregar(self, ruta, vel = 0, sentido = -1, x = 0, y = 0):

        capa = pilas.actores.Actor(ruta, x = x, y = y)
        copia_capa = pilas.actores.Actor(ruta, x = x, y = y)  
        
        if vel != 0:                
            t = (capa, copia_capa, vel, sentido)
            self.capas.append(t)
            if sentido == -1:            
                capa.x = 0
                copia_capa.x = copia_capa.obtener_ancho() 
            else:
                capa.x -= capa.obtener_ancho() 
                copia_capa.x = 0
        
    def actualizar_pantalla(self):

        for i in self.capas:
            if i[3] == -1:
                if i[0].x <= -i[0].obtener_ancho():
                    i[0].x = 0

                i[0].x -= i[2]
                i[1].x = i[0].x + i[1].obtener_ancho()

            else:
                if i[0].x >= 0:
                    i[0].x = -i[0].obtener_ancho()

                i[0].x += i[2]
                i[1].x = i[0].x + i[1].obtener_ancho()
               
        return True
    




capas = layers()

capas.agregar('cielo.png')
capas.agregar('montes.png', 1, sentido = -1)
capas.agregar('pasto.png', 3, sentido = -1, y = -120)
capas.agregar('arboles.png', 5, sentido = -1, y = -90)


pilas.ejecutar()
