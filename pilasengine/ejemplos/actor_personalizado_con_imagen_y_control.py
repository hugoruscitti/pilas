import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()

class Patito(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "patito.png"

    def actualizar(self):
        if pilas.control.izquierda:
            self.x -= 5
            self.espejado = True
        elif pilas.control.derecha:
            self.x += 5
            self.espejado = False


pilas.fondos.Noche()
patito = Patito(pilas)
pilas.avisar("Usa el teclado para mover al patito.")
pilas.ejecutar()
