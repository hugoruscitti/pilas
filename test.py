# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()

superficie = pilas.imagenes.cargar_superficie(100, 100)

# dibujamos el cuerpo
superficie.circulo(50, 50, 40, color=pilas.colores.verdeoscuro, relleno=True)

# un ojo
superficie.circulo(35, 35, 10, color=pilas.colores.blanco, relleno=True)
superficie.circulo(32, 35, 5, color=pilas.colores.negro, relleno=True)

# el otro ojo
superficie.circulo(67, 35, 10, color=pilas.colores.blanco, relleno=True)
superficie.circulo(64, 35, 5, color=pilas.colores.negro, relleno=True)

a = pilas.actores.Actor(superficie)
a.rotacion = [360], 10
a.escala = [0.5]


pilas.ejecutar()
