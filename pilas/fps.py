#import pygame
import time
import pygame

class ___FPS:

    def __init__(self, fps, usar_modo_economico):
        pass

    def actualizar(self):
        time.sleep(1 / 40.0)

    def obtener_cuadros_por_segundo(self):
        return 0

class FPS:
    #print "Usando pygame en el modulo fps"

    def __init__(self, fps, usar_modo_economico):
        self.antes = self.ahora = pygame.time.get_ticks()
        self.frecuencia = 1000.0 / fps
        self.t_fps = self.ahora
        self.rendimiento = 0
        self.cuadros_por_segundo = "??"
        self.usar_modo_economico = usar_modo_economico

    def actualizar(self):
        retorno = 0
        self.ahora = pygame.time.get_ticks()

        dt = self.ahora - self.antes 

        while dt >= self.frecuencia:
            self.antes += self.frecuencia
            dt = self.ahora - self.antes 
            retorno += 1

            if self.ahora - self.t_fps > 1000.0:
                #print self.cuadros_por_segundo
                self.cuadros_por_segundo = str(self.rendimiento)
                self.t_fps += 1000.0
                self.rendimiento = 0
        else:
            if self.usar_modo_economico:
                pygame.time.wait(int(self.frecuencia - dt))
            else:
                pygame.time.delay(int(self.frecuencia - dt))

            returno = 1


        self.rendimiento += 1
        return retorno


    def obtener_cuadros_por_segundo(self):
        return self.cuadros_por_segundo
