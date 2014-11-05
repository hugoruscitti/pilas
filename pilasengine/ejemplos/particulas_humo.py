# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')
import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(info=False)

emisor = pilas.actores.Emisor(0, 0)
emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
emisor.constante = True
emisor.composicion = "blanco"
emisor.duracion = 4

# Permite cambiar la posición del emisor de partículas.
def cuando_hace_click(evento):
    if -100 < evento.x < 100:
        emisor.x = [evento.x], 0.25
        emisor.y = [evento.y], 0.25

pilas.eventos.click_de_mouse.conectar(cuando_hace_click)


# Creando el controlador de propiedades para el emisor.
pc1 = pilas.actores.Controlador()
pc1.x = -150
pc1.y = 200

pc1.agregar(emisor, 'frecuencia_creacion', 0.01, 1)
pc1.agregar(emisor, 'vida', 0.1, 10)
pc1.agregar_espacio()

pc1.agregar(emisor, 'escala_fin_min', 0.1, 3)
pc1.agregar(emisor, 'escala_fin_max', 0.1, 3)
pc1.agregar(emisor, 'rotacion_fin_min', -360*2, 360*2)
pc1.agregar(emisor, 'rotacion_fin_max', -360*2, 360*2)
pc1.agregar(emisor, 'transparencia_fin_min', 0, 100)
pc1.agregar(emisor, 'transparencia_fin_max', 0, 100)
pc1.agregar_espacio()


pc1.agregar(emisor, 'aceleracion_x_min', -50, 50)
pc1.agregar(emisor, 'aceleracion_x_max', -50, 50)
pc1.agregar(emisor, 'aceleracion_y_min', -50, 50)
pc1.agregar(emisor, 'aceleracion_y_max', -50, 50)

pc1.agregar_espacio()


# Creando el controlador de propiedades para el emisor.
pc2 = pilas.actores.Controlador()
pc2.x = 230
pc2.y = 200

pc2.agregar(emisor, 'dy_min', -50, 50)
pc2.agregar(emisor, 'dy_max', -50, 50)
pc2.agregar_espacio()

pc2.agregar(emisor, 'dx_min', -20, 20)
pc2.agregar(emisor, 'dx_max', -20, 20)
pc2.agregar_espacio()

pc2.agregar(emisor, 'escala_min', 0.1, 4)
pc2.agregar(emisor, 'escala_max', 0.1, 4)
pc2.agregar_espacio()

pc2.agregar(emisor, 'rotacion_min', -360*2, 360*2)
pc2.agregar(emisor, 'rotacion_max', -360*2, 360*2)
pc2.agregar_espacio()

pc2.agregar(emisor, 'transparencia_min', 0, 100)
pc2.agregar(emisor, 'transparencia_max', 0, 100)
pc2.agregar_espacio()

pc2.agregar(emisor, 'x_min', -200, 200)
pc2.agregar(emisor, 'x_max', -200, 200)
pc2.agregar_espacio()

pc2.agregar(emisor, 'y_min', -200, 200)
pc2.agregar(emisor, 'y_max', -200, 200)
pc2.agregar_espacio()


pilas.avisar(u"Puedes hacer click para cambiar la posición del emisor")
pilas.ejecutar()
