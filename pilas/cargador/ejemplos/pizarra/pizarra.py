import pilas
import sys

pilas.iniciar()
pizarra = pilas.actores.Pizarra()

def dibujar_en_la_pizarra(evento):
    pizarra.dibujar_punto(evento.x, evento.y, pilas.colores.negro)

pilas.eventos.mueve_mouse.connect(dibujar_en_la_pizarra)

pilas.avisar("Usa el mouse para dibujar circulos.")
pilas.ejecutar()
