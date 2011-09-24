# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
 
import math
import pilas

class Comportamiento(object):
    "Representa un comportamiento (estrategia) que se puede anexar a un actor."
    
    def iniciar(self, receptor):
        "Se invoca cuando se anexa el comportamiento a un actor."
        self.receptor = receptor

    def actualizar(self):
        """Actualiza el comportamiento en un instante dado.

        Si este metodo retorna True entonces el actor dejará
        de ejecutar este comportamiento."""
        pass

    def terminar(self):
        pass


class Girar(Comportamiento):
    "Hace girar constantemente al actor respecto de su eje de forma relativa."

    def __init__(self, delta, velocidad):
        self.delta = delta

        if delta > 0:
            self.velocidad = velocidad
        else:
            self.velocidad = -velocidad


    def iniciar(self, receptor):
        "Define el angulo inicial."
        self.receptor = receptor
        self.angulo_final = (receptor.rotacion + self.delta) % 360

    def actualizar(self):
        self.receptor.rotacion += self.velocidad

        delta = abs(self.receptor.rotacion - self.angulo_final)

        if delta <= abs(self.velocidad):
            self.receptor.rotacion = self.angulo_final
            return True

class Saltar(Comportamiento):

    def __init__(self, velocidad_inicial=10, cuando_termina=None):
        self.velocidad_inicial = velocidad_inicial
        self.cuando_termina = cuando_termina
        self.sonido_saltar = pilas.sonidos.cargar("saltar.wav")

    def iniciar(self, receptor):
        self.receptor = receptor
        self.suelo = int(self.receptor.y)
        self.velocidad = self.velocidad_inicial
        self.sonido_saltar.reproducir()

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3

        if self.receptor.y <= self.suelo:
            self.velocidad_inicial /= 2.0
            self.velocidad = self.velocidad_inicial
            
            if self.velocidad_inicial <= 1:
                # Si toca el suelo
                self.receptor.y = self.suelo
                if self.cuando_termina:
                    self.cuando_termina()
                return True


class Avanzar(Comportamiento):
    "Desplaza al actor en la dirección y sentido indicado por una rotación."

    def __init__(self, pasos, velocidad=5):
        self.pasos = abs(pasos)
        self.velocidad = velocidad

    def iniciar(self, receptor):
        self.receptor = receptor
        rotacion_en_radianes = math.radians(-receptor.rotacion)
        self.dx = math.cos(rotacion_en_radianes)
        self.dy = math.sin(rotacion_en_radianes)

    def actualizar(self):
        salir = False

        if self.pasos - self.velocidad < 0:
            avance = self.pasos
            salir = True
        else:
            avance = self.velocidad

        self.pasos -= avance
        self.receptor.x += self.dx * avance
        self.receptor.y += self.dy * avance

        if salir:
            return True
