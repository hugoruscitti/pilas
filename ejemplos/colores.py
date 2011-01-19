import pilas

pilas.iniciar()

pizarra = pilas.actores.Pizarra()


# Selecciona solamente a los atributos que parecen colores.
colores = [color for color in dir(pilas.colores) if not '_' in color and not color == 'pilas']

# Por cada color imprime su nombre y un rectangulo de su color.
for indice, color in enumerate(colores):
    dy = 200 - indice * 23
    pizarra.definir_color(getattr(pilas.colores, color))
    pizarra.dibujar_rectangulo(80, dy, 20, 20)

    pizarra.definir_color(pilas.colores.negro)
    pizarra.escribir(color, -100, dy - 15, tamano=10)

pilas.ejecutar()
