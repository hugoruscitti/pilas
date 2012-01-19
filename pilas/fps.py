# -*- encoding: utf-8 -*-
import time
from PyQt4 import QtCore


class _FPS(object):

    def __init__(self, fps, usar_modo_economico):
        self.antes = self.ahora = pygame.time.get_ticks()
        self.frecuencia = 1000.0 / fps
        self.t_fps = self.ahora
        self.rendimiento = 0
        self.cuadros_por_segundo = "??"
        self.usar_modo_economico = usar_modo_economico
        self.inicial = time.time()

    def actualizar(self):
        retorno = 0
        self.ahora = pygame.time.get_ticks()
        # a la velocidad de los segundos, mill por segundo
        #print self.ahora, time.time() - self.inicial

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
                #time.sleep(1)
                pygame.time.wait(int(self.frecuencia - dt))
                #pygame.time.wait(0)
            else:
                pass
                #pygame.time.delay(int(self.frecuencia - dt))

            returno = 1


        self.rendimiento += 1
        return retorno


    def obtener_cuadros_por_segundo(self):
        return self.cuadros_por_segundo


# parece que hay que usar time.time en unix y time.clock en windows

class FPS(object):

    def __init__(self, fps, usar_modo_economico):
        self.cuadros_por_segundo = "??"
        self.frecuencia = 1000.0 / fps
        self.timer = QtCore.QTime()
        self.timer.start()
        self.siguiente = self.timer.elapsed() + self.frecuencia
        self.cuadros = 0
        self.ultimo_reporte_fps = 0

    def actualizar(self):
        actual = self.timer.elapsed()

        if actual > self.siguiente:
            cantidad = 0

            while actual > self.siguiente:
                self.siguiente += self.frecuencia
                cantidad += 1
                self._procesar_fps(actual)

            if cantidad > 10:
                cantidad = 10

            self.cuadros += 1
            return cantidad
        else:
            # wait
            return 0

    def _procesar_fps(self, actual):
        if actual - self.ultimo_reporte_fps > 1000.0:
            self.ultimo_reporte_fps += 1000.0
            self.cuadros_por_segundo = str(self.cuadros)
            self.cuadros = 0


        #sleepTime = self.frecuencia - (newTime - self.delay)
        #if sleepTime > 0:
        #    time.sleep(sleepTime)
        #self.delay = newTime
        #return 1

        """




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
                #time.sleep(1)
                pygame.time.wait(int(self.frecuencia - dt))
                #pygame.time.wait(0)
            else:
                pass
                #pygame.time.delay(int(self.frecuencia - dt))

            returno = 1


        self.rendimiento += 1
        return retorno
        """


    def obtener_cuadros_por_segundo(self):
        return self.cuadros_por_segundo
