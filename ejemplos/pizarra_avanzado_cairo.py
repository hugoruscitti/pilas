import pilas
import sys

pilas.iniciar()

# paso 1: crear la pizarra
pizarra = pilas.actores.Pizarra()

# paso 2: comienza el dibujo personalizado con cairo:
import cairo

x1, y1 = (100, 100)
x2, y2 = (600, 300)
x3, y3 = (100, 400)

pizarra.canvas.context.curve_to(x1, y1, x2, y2, x3, y3)
pizarra.canvas.context.set_line_width(50)
pizarra.canvas.context.set_dash([10])
pizarra.canvas.context.stroke()

# paso 3: Decirle a la pizarra que se actualice.
pizarra.actualizar_imagen()

pilas.ejecutar()
