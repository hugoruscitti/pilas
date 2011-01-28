# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class layers:
    def __init__(self, modo = 'automatico'):
        self.capas = []
        if modo == 'automatico':
            pilas.mundo.agregar_tarea(0, self.actualizar_pantalla)
        elif modo == 'manual':
            pass

        self.estado = modo


    
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

    def mover_derecha(self):
        if self.estado == 'manual':
            for i in self.capas:
                if i[0].x <= -i[0].obtener_ancho():
                    i[0].x = 0

                i[0].x -= i[2]
                i[1].x = i[0].x + i[1].obtener_ancho()

    def mover_izquierda(self):
        
        if self.estado == 'manual':
            for i in self.capas:
                if i[0].x >= 0:
                    i[0].x = -i[0].obtener_ancho()

                i[0].x += i[2]
                i[1].x = i[0].x + i[1].obtener_ancho()

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
    






