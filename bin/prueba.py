import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)

pilas.depurador.definir_modos(posiciones=True)
a = pilas.actores.CursorDisparo()
a.z = -100

class Actor(pilasengine.actores.Actor):

    def actualizar(self):
        self.x += pilas.pad.x * 6
        self.y += pilas.pad.y * 6
        a.x = pilas.pad.x1 * 300
        a.y = pilas.pad.y1 * 300


actor = Actor(pilas)
actor.imagen = "aceituna.png"


bananas = pilas.actores.Banana() * 30
bananas.radio_de_colision = 20


def eliminar(a, b):
    b.eliminar()
    a.escala_x = [1.4, 1],0.05
    a.escala_y = [1.5, 1],0.09

pilas.colisiones.agregar(actor, bananas, eliminar)
pilas.ejecutar()