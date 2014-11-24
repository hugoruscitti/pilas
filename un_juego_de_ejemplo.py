import pilasengine

pilas = pilasengine.iniciar()

class Alien(pilasengine.actores.Actor):

    def iniciar(self, x, y):
        self.imagen = "alien.png"
        self.velocidad = 10
        self.x = x
        self.y = y
        self.rotacion = [360],10
        self.y = [y+-200],10

    def saludar(self):
        self.decir("Hola mundo!!!, soy el nuevo actor alien")

    def dar_vuelta(self):
        self.rotacion = [360]

    def actualizar(self):
        if pilas.control.izquierda:
            self.x -= 5
            self.espejado = True
        if pilas.control.derecha:
            self.x += 5
            self.espejado = False


pilas.actores.Actor(x=100, y=100)
alien = Alien(pilas, x=100, y=200)


pilas.ejecutar()
