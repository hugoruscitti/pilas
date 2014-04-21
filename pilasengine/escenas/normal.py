from pilasengine.escenas.escena import Escena

class Normal(Escena):

    def iniciar(self):
        self.fondo = self.pilas.fondos.Plano()

    def actualizar(self):
        pass

    def terminar(self):
        pass