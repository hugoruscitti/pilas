import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)

pilas.depurador.definir_modos(posiciones=False)

class Sombra(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = pilas.imagenes.cargar_grilla('sombra.png', 10, 1)

    def actualizar(self):
        self.imagen.avanzar(24)

class Vaca(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = pilas.imagenes.cargar_grilla('animacion.png', 10, 1)
        self.sombra = Sombra(pilas)

    def actualizar(self):
        self.imagen.avanzar(24)
        self.sombra.actualizar()
        self.sombra.x = self.x
        self.sombra.y = self.y - 60


a = Vaca(pilas)
a.z = -100

class Actor(pilasengine.actores.Actor):

    def actualizar(self):
        self.mover_actor(self, pilas.pad.x, pilas.pad.y)
        self.mover_actor(a, pilas.pad.x1, pilas.pad.y1)

    def mover_actor(self, actor, x, y):
        actor.x += x * 6
        actor.y += y * 6

        if actor.x < -320:
            actor.x = -320
        elif actor.x > 320:
            actor.x = 320

        if actor.y > 240:
            actor.y = 240
        elif actor.y < -240:
            actor.y = -240



actor = Actor(pilas)
actor.imagen = "aceituna.png"

bananas = pilas.actores.Banana() * 30
bananas.radio_de_colision = 20

cantidad = len(bananas)
barra = pilas.actores.Energia(y=-200, progreso=0)


def eliminar(a, b):
    b.eliminar()
    a.escala_x = [1.4, 1],0.05
    a.escala_y = [1.5, 1],0.09
    barra.progreso += 100.0/cantidad

pilas.colisiones.agregar(actor, bananas, eliminar)
pilas.ejecutar()