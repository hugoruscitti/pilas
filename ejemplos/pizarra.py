import pilas
import sys

pilas.iniciar()
pizarra = pilas.actores.Pizarra()

def dibujar_en_la_pizarra(sender, x, y, signal, dx, dy):
    pizarra.dibujar_cuadrado(x, y)

pilas.eventos.mueve_mouse.connect(dibujar_en_la_pizarra)

pilas.avisar("Usa el mouse para dibujar.")
pilas.ejecutar()
