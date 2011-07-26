import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()

pizarra = pilas.actores.Pizarra()


# Selecciona solamente a los atributos que parecen colores.
colores = [color for color in dir(pilas.colores) if not '_' in color and not color == 'pilas' and not color == "Color"]

# Por cada color imprime su nombre y un rectangulo de su color.
for indice, color in enumerate(colores):
    dy = 30 + indice * 23 - 170
    pizarra.rectangulo(0, dy, 20, 20, getattr(pilas.colores, color), relleno=True)
    pizarra.rectangulo(0, dy, 20, 20, color=pilas.colores.negro)
    pizarra.texto(color, 30, dy - 15)

pilas.avisar("Muestra los colores mas usados del modulo pilas.colores")
pilas.ejecutar()
