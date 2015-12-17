import pilasengine
pilas = pilasengine.iniciar()

VELOCIDAD = 6

class Vampiro(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = pilas.imagenes.cargar_animacion("imagenes/protagonista.png", 6)
        self.y = -155
        self.escala = 0.75
        self.radio_de_colision = 30

        self.imagen.definir_animacion('parado', [2], 10)
        self.imagen.definir_animacion('caminar', [3, 4, 5, 4], 15)
        self.imagen.definir_animacion('saltar', [0], 15)

        self.hacer_inmediatamente('ComportamientoNormal')

    def actualizar(self):
        if pilas.control.izquierda:
            self.x -= VELOCIDAD
            self.espejado = True

        if pilas.control.derecha:
            self.x += VELOCIDAD
            self.espejado = False

        if self.x > 280:
            self.x = 280

        if self.x < -280:
            self.x = -280

        self.imagen.avanzar()


class ComportamientoNormal(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('parado')

    def actualizar(self):
        if pilas.control.derecha or pilas.control.izquierda:
            self.receptor.hacer_inmediatamente('ComportamientoCaminar')

        if pilas.control.arriba:
            self.receptor.hacer_inmediatamente('ComportamientoSaltar')


class ComportamientoCaminar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('caminar')

    def actualizar(self):
        if not pilas.control.derecha and not pilas.control.izquierda:
            self.receptor.hacer_inmediatamente('ComportamientoNormal')

        if pilas.control.arriba:
            self.receptor.hacer_inmediatamente('ComportamientoSaltar')

class ComportamientoSaltar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('saltar')
        self.velocidad = 12
        self.coordenada_y_inicial = self.receptor.y

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.5

        if self.receptor.y < self.coordenada_y_inicial:
            self.receptor.hacer_inmediatamente('ComportamientoNormal')
            self.receptor.y = self.coordenada_y_inicial


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
pilas.comportamientos.vincular(ComportamientoNormal)
pilas.comportamientos.vincular(ComportamientoCaminar)
pilas.comportamientos.vincular(ComportamientoSaltar)


def crear_calabaza():
    calabaza = pilas.actores.Calabaza()

pilas.tareas.siempre(2, crear_calabaza)

########

pilas.actores.vincular(Vampiro)

vampiro = pilas.actores.Vampiro()
pilas.fondos.Fondo("imagenes/fondo.png")

pilas.ejecutar()
