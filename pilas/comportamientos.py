# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
 
import math
import pilas

class Comportamiento:
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
    "Hace girar constantemente al actor respecto de su eje."

    def __init__(self):
        self.angulo = 0

    def actualizar(self):
        self.angulo += 1
        self.receptor.rotacion = self.angulo


class Avanzar(Comportamiento):
    "Desplaza al actor en la dirección y sentido indicado por una rotación."

    def __init__(self, rotacion_en_grados, pasos):
        rotacion_en_radianes = math.radians(rotacion_en_grados)
        self.pasos = pasos
        self.dx = math.cos(rotacion_en_radianes)
        self.dy = math.sin(rotacion_en_radianes)

    def iniciar(self, receptor):
        self.receptor = receptor
        self.to_x = (self.dx * self.pasos) + receptor.x
        self.to_y = (self.dy * self.pasos) + receptor.y

    def actualizar(self):
        distancia_x = pilas.utils.distancia(self.receptor.x, self.to_x)
        distancia_y = pilas.utils.distancia(self.receptor.y, self.to_y)

        velocidad = 10

        # Avanza en la direccion al punto destino y no lo sobrepasa.
        self.receptor.x += min(self.dx * velocidad, distancia_x)
        self.receptor.y += min(self.dy * velocidad, distancia_y)

        # Termina el movimiento llega al punto destino.
        if distancia_x < 1 and distancia_y < 1:
            return True
