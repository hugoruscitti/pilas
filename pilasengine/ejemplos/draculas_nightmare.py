import pilasengine
pilas = pilasengine.iniciar()

class Vampiro(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "imagenes/vampiro.png"
        self.y = -155
        self.escala = 0.75
        self.radio_de_colision = 30

    def actualizar(self):
        if pilas.control.izquierda:
            self.x -= 8
            self.espejado = True

        if pilas.control.derecha:
            self.x += 8
            self.espejado = False

        if self.x > 250:
            self.x = 250

        if self.x < -250:
            self.x = -250

########
class Calabaza(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "imagenes/calabaza.png"
        self.y = 300
        self.x = pilas.azar(-250, 250)
        self.velocidad = 0
        self.radio_de_colision = 50
        self.escala = 0.70

    def actualizar(self):
        self.velocidad += 0.05
        self.y -= self.velocidad
        self.rotacion += 2

        if self.y < -400:
            self.eliminar()

pilas.actores.vincular(Calabaza)


def crear_calabaza():
    calabaza = pilas.actores.Calabaza()

pilas.tareas.siempre(2, crear_calabaza)

########

pilas.actores.vincular(Vampiro)

vampiro = pilas.actores.Vampiro()
pilas.fondos.Fondo("imagenes/fondo.png")

pilas.ejecutar()
