# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento



class Shaolin(Actor):
    """Representa un luchador que se puede controlar con el teclado,
    puede saltar, golpear y recibir golpes."""

    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.hacer_inmediatamente(Parado)
        self.sombra = self.pilas.actores.Sombra()
        self.altura_del_salto = 0
        
    def actualizar(self):
        self.sombra.x = self.x
        self.sombra.z = self.z + 1
        self.sombra.rotacion = self.rotacion
        
        # Adapta el tamaño y la distancia a la sombra para simular
        # que la sombra está siempre 'pegada' al suelo del escenario.
        self.sombra.y = self.y + 10 - self.altura_del_salto
        self.sombra.escala = self.escala - self.altura_del_salto / 300.0

class Parado(Comportamiento):

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.control = receptor.pilas.control

        self.receptor.imagen = self.pilas.imagenes.cargar_grilla("shaolin/parado.png", 4, 1)
        self.receptor.centro = ("centro", "abajo")

    def actualizar(self):
        self.receptor.imagen.avanzar(10)
        
        # Si pulsa a los costados comienza a caminar.
        if self.control.derecha or self.control.izquierda:
            self.receptor.hacer_inmediatamente(Caminar)
            
        # Si pulsa hacia arriba salta.
        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltar)

class Caminar(Comportamiento):
    
    def iniciar(self, receptor):
        self.receptor = receptor
        self.control = receptor.pilas.control

        self.receptor.imagen = self.pilas.imagenes.cargar_grilla("shaolin/camina.png", 4, 1)
        self.receptor.centro = ("centro", "abajo")
        
    def actualizar(self):
        self.receptor.imagen.avanzar(10)
        
        # Si pulsa a los costados se puede mover.
        if self.control.derecha:
            self.receptor.x += 5
            self.receptor.espejado = False
        elif self.control.izquierda:
            self.receptor.x -= 5
            self.receptor.espejado = True
            
        # Si pulsa hacia arriba salta.
        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltar)
            
        # Si suelta las teclas regresa al estado inicial.
        if not self.control.derecha and not self.control.izquierda:
            self.receptor.hacer_inmediatamente(Parado)
            
class Saltar(Comportamiento):
    
    def iniciar(self, receptor):
        self.receptor = receptor
        self.control = receptor.pilas.control

        self.receptor.imagen = self.pilas.imagenes.cargar_grilla("shaolin/salta.png", 3, 1)
        self.receptor.centro = ("centro", "abajo")
        self.y_inicial = self.receptor.y
        self.vy = 15
        
    def actualizar(self):
        self.receptor.y += self.vy
        self.vy -= 0.7

        distancia_al_suelo = self.receptor.y - self.y_inicial
        self.receptor.altura_del_salto = distancia_al_suelo

        # Cuando llega al suelo, regresa al estado inicial.
        if distancia_al_suelo < 0:
            self.receptor.y = self.y_inicial
            self.receptor.altura_del_salto = 0
            self.receptor.hacer_inmediatamente(Parado)
            
        # Si pulsa a los costados se puede mover.
        if self.control.derecha:
            self.receptor.x += 5
            self.receptor.espejado = False
        elif self.control.izquierda:
            self.receptor.x -= 5
            self.receptor.espejado = True