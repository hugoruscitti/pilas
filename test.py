# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()

t = pilas.actores.Tortuga()

'''
superficie = pilas.imagenes.cargar_superficie(100, 100)

# dibujamos el cuerpo
superficie.circulo(50, 50, 40, color=pilas.colores.verdeoscuro, relleno=True)

# dibujamos el borde del cuerpo
superficie.circulo(50, 50, 40, color=pilas.colores.negro, relleno=False, grosor=2)

# un ojo
superficie.circulo(35, 35, 10, color=pilas.colores.blanco, relleno=True)
superficie.circulo(32, 35, 5, color=pilas.colores.negro, relleno=True)

# el otro ojo
superficie.circulo(67, 35, 10, color=pilas.colores.blanco, relleno=True)
superficie.circulo(64, 35, 5, color=pilas.colores.negro, relleno=True)

superficie.pintar(pilas.colores.blanco)
superficie.texto("Hola mundo", magnitud=20, fuente="Courrier", color=pilas.colores.rojo)
a = pilas.actores.Actor(superficie)
'''


pilas.ejecutar()
