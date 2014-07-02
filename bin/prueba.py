import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)

pilas.depurador.definir_modos()

class Actor(pilasengine.actores.Actor):

    def actualizar(self):
        self.x += pilas.pad.x * 6
        self.y += pilas.pad.y * 6
        self.rotacion = (pilas.pad.x1 -1) * 180


actor = Actor(pilas)
actor.imagen = "aceituna.png"


bananas = pilas.actores.Banana() * 30


def eliminar(a, b):
    b.eliminar()
    a.escala_x = [a.escala+1, a.escala],0.05
    a.escala_y = [a.escala+1, a.escala],0.09

pilas.colisiones.agregar(actor, bananas, eliminar)
pilas.ejecutar()