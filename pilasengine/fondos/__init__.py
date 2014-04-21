# -*- encoding: utf-8 -*-

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
        return self.pilas.actores.agregar_actor(nuevo_fondo)