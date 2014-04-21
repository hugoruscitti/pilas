from pilasengine.fondos.fondo import Fondo

class Plano(Fondo):

    def iniciar(self):
        self.imagen = "fondos/plano.png"

    def dibujar(self, painter):
        painter.save()

        x = self.pilas.obtener_escena_actual().camara.x
        y = -self.pilas.obtener_escena_actual().camara.y

        ancho, alto = self.pilas.obtener_area()
        painter.drawTiledPixmap(0, 0, ancho, alto, self.imagen._imagen, x % 30, y % 30)

        painter.restore()