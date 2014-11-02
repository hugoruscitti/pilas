import pilas
import random

class PiedraEspacial(pilas.actores.Piedra):
    "Representa una piedra espacial que se puede romper con un disparo."

    def __init__(self, piedras, x=0, y=0, tamano="grande"):
        # Obtiene una velocidad de movimiento aleatoria.
        posibles_velocidades = list(range(-10, -2)) + list(range(2, 10))

        dx = random.choice(posibles_velocidades) / 10.0
        dy = random.choice(posibles_velocidades) / 10.0

        pilas.actores.Piedra.__init__(self, x=x, y=y, dx=dx, dy=dy, tamano=tamano)
        self.tamano = tamano
        self.piedras = piedras

    def eliminar(self):
        "Este metodo se invoca cuando el disparo colisiona con la nave."
        explosion = pilas.actores.Explosion(self.x, self.y)
        pilas.actores.Piedra.eliminar(self)

        if self.tamano == "grande":
            self.crear_dos_piedras_mas_pequenas(self.x, self.y, "media")
        elif self.tamano == "media":
            self.crear_dos_piedras_mas_pequenas(self.x, self.y, "chica")

    def crear_dos_piedras_mas_pequenas(self, x, y, tamano):
        "Genera dos piedras mas chicas, enemigas de la nave."
        piedra_1 = PiedraEspacial(self.piedras, x=x, y=y, tamano=tamano)
        piedra_2 = PiedraEspacial(self.piedras, x=x, y=y, tamano=tamano)
        self.piedras.append(piedra_1)
        self.piedras.append(piedra_2)
