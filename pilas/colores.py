import pilas

class Color(object):
    "Representa un color en base a 4 componentes."

    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def obtener(self):
        return pilas.motor.Color(self.r, self.g, self.b, self.a)

    def __str__(self):
        return "<Color (%d, %d, %d, %d)>" %(self.r, self.g, self.b, self.a)

    def obtener_componentes(self):
        return (self.r, self.g, self.b, self.a)

# Colores principales.
negro = Color(0, 0, 0)
blanco = Color(255, 255, 255)
rojo = Color(255, 0, 0)
verde = Color(0, 255, 0)
azul = Color(0, 0, 255)
gris = Color(128, 128, 128)


# Colores secundarios
amarillo = Color(255, 255, 0)
magenta = Color(255, 0, 255)
cyan = Color(0, 255, 255)
grisclaro = Color(192, 192, 192)
grisoscuro = Color(100, 100, 100)
verdeoscuro = Color(0, 128, 0)
azuloscuro = Color(0, 0, 128)
naranja = Color(255, 200, 0)
rosa = Color(255, 175, 175)
violeta = Color(128, 0, 255)
marron = Color(153, 102, 0)

# Colores transparentes
negro_transparente = Color(0, 0, 0, 160)
blanco_transparente = Color(255, 255, 255, 160)
rojo_transparente = Color(255, 0, 0, 160)
verde_transparente = Color(0, 255, 0, 160)
azul_transparente = Color(0, 0, 255, 160)
gris_transparente = Color(128, 128, 128, 160)
