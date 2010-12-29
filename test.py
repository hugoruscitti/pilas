import pilas
import pilas.elements as elements

pilas.iniciar()
size = (640, 480)
mundo = elements.Elements(screen_size=size, renderer="cairo")

b = pilas.actores.Pizarra()

b1 = mundo.add.ball((101, 101), 20)
b1 = mundo.add.ball((120, 0), 20)
v2 = mundo.add.triangle((120, 0), 20)
v3 = mundo.add.rect((120, 0), 20, 30)
v4 = mundo.add.wall((0, 200), (400, 300))


mundo.renderer.set_pizarra(b)
mundo.add.ground()

class Actor(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self)

    def actualizar(self):
        mundo.update()
        mundo.draw()
        b.actualizar_imagen()
        pass



a = Actor()

pilas.ejecutar()
