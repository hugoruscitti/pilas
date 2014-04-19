from pilasengine.actores.actor import Actor

class Mono(Actor):

    def iniciar(self):
        self.imagen = "mono.png"

    def actualizar(self):
        self.rotacion += 3
        self.x += 1
        self.y += 1