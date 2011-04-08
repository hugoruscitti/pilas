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
    dy = 30 + indice * 23
    pizarra.definir_color(getattr(pilas.colores, color))
    pizarra.dibujar_rectangulo(80, dy, 20, 20)

    pizarra.definir_color(pilas.colores.negro)
    pizarra.escribir(color, 130, dy + 15, tamano=10)

pilas.avisar("Muestra los colores mas usados del modulo pilas.colores")
pilas.ejecutar()
