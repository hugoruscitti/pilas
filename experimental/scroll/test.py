import pilas
pilas.iniciar()


class FondoCiclico(pilas.actores.Actor):

    def __init__(self, x=0, y=0, ancho_pantalla=640):
        pilas.actores.Actor.__init__(self)
        self.imagen = "scroll.png"
        self.centro = ("izquierda", "arriba")
        self.ancho_pantalla = ancho_pantalla
        self.x = x
        self.y = y

    def actualizar(self):
        self.x -= 4

        if self.ancho + self.x < - self.ancho_pantalla:
            self.x = 0


FondoCiclico(160)
pizarra = pilas.actores.Pizarra()
pizarra.rectangulo(0, 0, 160, 120)

    

pilas.ejecutar()
