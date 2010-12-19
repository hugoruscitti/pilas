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

        #self.to_x = (self.dx * self.pasos) + receptor.x
        #self.to_y = (self.dy * self.pasos) + receptor.y

    def actualizar(self):
        self.pasos -= 1

        if self.pasos < 0:
            return True

        self.receptor.x += self.dx
        self.receptor.y += self.dy

        #distancia_x = pilas.utils.distancia(self.receptor.x, self.to_x)
        #distancia_y = pilas.utils.distancia(self.receptor.y, self.to_y)

        # Avanza en la direccion al punto destino y no lo sobrepasa.
        #self.receptor.x += min(self.dx * self.velocidad, distancia_x)
        #self.receptor.y += min(self.dy * self.velocidad, distancia_y)

        # Termina el movimiento llega al punto destino.
        #if distancia_x < self.velocidad + 1 and distancia_y < self.velocidad + 1:
        #    return True

class CambiarColor(Comportamiento):
    "Llama a un metodo para cambiar el color de un actor."

    def __init__(self, nuevo_color):
        self.nuevo_color = nuevo_color

    def iniciar(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        self.receptor.color = self.nuevo_color
        return True
