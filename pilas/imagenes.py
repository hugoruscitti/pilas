# License: Public Domain
# Author: Hugo Ruscitti (http://www.losersjuegos.com.ar)

from PySFML import sf
import pilas

class Grilla:

    def __init__(self, ruta, columnas=1, filas=1):
        self.image = pilas.imagen.cargar(ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = self.image.GetWidth() / columnas
        self.cuadro_alto = self.image.GetHeight() / filas
        self.sub_rect = sf.IntRect(0, 0, self.cuadro_ancho, self.cuadro_alto)
        self.definir_cuadro(0)

    def definir_cuadro(self, cuadro):
        self.cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        dx = frame_col * self.cuadro_ancho - self.sub_rect.Left
        dy = frame_row * self.cuadro_alto - self.sub_rect.Top

        self.sub_rect.Offset(dx, dy)

    def asignar(self, sprite):
        "Sets the sprite's image with animation state."

        sprite.SetImage(self.image)
        sprite.SetSubRect(self.sub_rect)

    def avanzar(self):
        ha_reiniciado = False
        cuadro_actual = self.cuadro + 1

        if cuadro_actual >= self.cantidad_de_cuadros:
            cuadro_actual = 0
            ha_reiniciado = True

        self.definir_cuadro(cuadro_actual)
        return ha_reiniciado

    def obtener_cuadro(self):
        return self.cuadro
