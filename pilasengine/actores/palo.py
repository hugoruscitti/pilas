from pilasengine.actores.actor import Actor

class Palo(Actor):

    def iniciar(self):
        self.imagen = "palo.png"
        self.centro = (0, "centro")

    def actualizar(self):
        pass

    def terminar(self):
        pass