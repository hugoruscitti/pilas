# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class Fondo(pilas.actores.Actor):

    def __init__(self, imagen):
        pilas.actores.Actor.__init__(self, imagen)
        self.z = 1000

class Volley(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/volley.jpg")

class Nubes(Fondo):
    "Muestra un fondo celeste con nubes."

    def __init__(self):
        Fondo.__init__(self, "fondos/nubes.png")

class Pasto(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/pasto.png")

class Selva(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/selva.jpg")


class Tarde(Fondo):
    "Representa una escena de fondo casi naranja."

    def __init__(self):
        Fondo.__init__(self, "fondos/tarde.jpg")


class Espacio(Fondo):
    "Es un espacio con estrellas."

    def __init__(self):
        Fondo.__init__(self, "fondos/espacio.jpg")

class Noche(Fondo):
    "Muestra una escena que tiene un fondo de pantalla de paisaje."

    def __init__(self):
        Fondo.__init__(self, "fondos/noche.jpg")

class Color(Fondo):
    "Pinta todo el fondo de un color uniforme."
    
    def __init__(self, color):
        Fondo.__init__(self, "invisible.png")
        self.color = color
        self.lienzo = pilas.imagenes.cargar_lienzo()

    def dibujar(self, motor):
        if self.color:
            self.lienzo.pintar(motor, self.color)


class Desplazamiento(Fondo):
    """Representa un fondo formado por varias capas (o actores).

    En fondo de este tipo, ayuda a generar un efecto de profundidad,
    de perspectiva en tres dimensiones.
    """

    def __init__(self, ciclico=True):
        "Inicia el objeto, dando la opción de simular que el fondo es infinitio"

        Fondo.__init__(self, "invisible.png")
        self.posicion = 0
        self.posicion_anterior = 0
        self.capas = []
        self.velocidades = {}
        pilas.eventos.mueve_camara.conectar(self.cuando_mueve_camara)
        self.ciclico = True

        if ciclico:
            self.capas_auxiliares = []

    def agregar(self, capa, velocidad=1):
        x, _, _, y = pilas.utils.obtener_bordes()
        capa.fijo = True
        capa.izquierda = x

        self.capas.append(capa)
        self.velocidades[capa] = velocidad

        if self.ciclico:
            copia = capa.duplicar()
            copia.fijo = True
            copia.imagen = capa.imagen
            self.capas_auxiliares.append(copia)
            copia.izquierda = capa.derecha
            self.velocidades[copia] = velocidad

    def actualizar(self):
        if self.posicion != self.posicion_anterior:
            dx = self.posicion - self.posicion_anterior
            self.mover_capas(dx)
            self.posicion_anterior = self.posicion
    
    def cuando_mueve_camara(self, evento):
        dx = evento.dx

        # Hace que las capas no se desplacen naturalmente
        # como todos los actores.
        #for x in self.capas:
        #    x.x += dx

        # aplica un movimiento respetando las velocidades.
        self.mover_capas(dx)

    def mover_capas(self, dx):
        for capa in self.capas:
            capa.x -= dx * self.velocidades[capa]

        if self.ciclico:
            for capa in self.capas_auxiliares:
                capa.x -= dx * self.velocidades[capa]
