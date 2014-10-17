import pilasengine

pilas = pilasengine.iniciar()


class Paleta(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = 'imagenes_bloques/paleta.png'
        self.x = 0
        self.y = -200
        self.figura_de_colision = pilas.fisica.Rectangulo(0,0, 100, 20, False)

    def actualizar(self):
        if self.pilas.control.izquierda:
            self.x -= 5

        elif self.pilas.control.derecha:
            self.x += 5

        if self.x <= -265:
            self.x = -265
        elif self.x >= 265:
            self.x = 265


class Ladrillo(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = 'imagenes_bloques/ladrillo.png'
        self.figura_de_colision = pilas.fisica.Rectangulo(0, 0, 60, 30, False)


def crear_ladrillo(grupo_ladrillos, x, y):
    ladrillo = Ladrillo(pilas)
    ladrillo.x = x
    ladrillo.y = y
    grupo_ladrillos.agregar(ladrillo)


def eliminar_ladrillo(pelota, ladrillo):
    ladrillo.eliminar()

def empujar_pelota(paleta, pelota):
    pelota.empujar((pelota.x - paleta.x) / 5.0, 10)


paleta = Paleta(pilas)


ladrillos = pilas.actores.Grupo()

crear_ladrillo(ladrillos, -200, 100)
crear_ladrillo(ladrillos, -100, 100)
crear_ladrillo(ladrillos,    0, 100)
crear_ladrillo(ladrillos,  100, 100)
crear_ladrillo(ladrillos,  200, 100)

# ladrillos.aprender(pilas.habilidades.Arrastrable)


pelota = pilas.actores.Pelota()
pelota.figura.escala_de_gravedad = 0
pelota.empujar(0, -10)
pelota.aprender(pilas.habilidades.Arrastrable)
#pelota.imagen = 'pelota_gris.png'

pilas.colisiones.agregar(paleta, pelota, empujar_pelota)
pilas.colisiones.agregar(pelota, ladrillos, eliminar_ladrillo)

## pilas.fisica.eliminar_suelo()

pilas.ejecutar()
