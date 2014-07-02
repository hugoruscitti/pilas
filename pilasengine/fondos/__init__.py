# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import colores


class Fondos(object):
    """Representa la propiedad pilas.fondos

    Este objeto se encarga de hacer accesible
    la creación de fondos para las escenas.
    """

    def __init__(self, pilas):
        self.pilas = pilas

    def Plano(self):
        import plano
        nuevo_fondo = plano.Plano(self.pilas)
        # Importante: cuando se inicializa el actor, el método __init__
        #             realiza una llamada a pilas.actores.agregar_actor
        #             para vincular el actor a la escena.
        return nuevo_fondo

    def Tarde(self):
        import tarde
        return tarde.Tarde(self.pilas)

    def Selva(self):
        import selva
        return selva.Selva(self.pilas)

    def Noche(self):
        import noche
        return noche.Noche(self.pilas)

    def Espacio(self):
        import espacio
        return espacio.Espacio(self.pilas)

    def Nubes(self):
        import nubes
        return nubes.Nubes(self.pilas)

    def Pasto(self):
        import pasto
        return pasto.Pasto(self.pilas)

    def Volley(self):
        import volley
        return volley.Volley(self.pilas)

    def Color(self, _color=colores.blanco):
        import color
        return color.Color(self.pilas, _color)

    def Blanco(self):
        import blanco
        return blanco.Blanco(self.pilas)

    def Fondo(self, imagen=None):
        import fondo
        return fondo.Fondo(self.pilas, imagen)