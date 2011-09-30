import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

class Patito(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self)
        self.imagen = "patito.png"

    def actualizar(self):
        if pilas.mundo.control.izquierda:
            self.x -= 5
            self.espejado = True
        elif pilas.mundo.control.derecha:
            self.x += 5
            self.espejado = False


pilas.fondos.Noche()
patito = Patito()
pilas.avisar("Usa el teclado para mover al patito.")
pilas.ejecutar()
