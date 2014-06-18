# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(info=True)

emisor = pilas.actores.Emisor(-100, 100)
emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
emisor.constante = True

# Permite cambiar la posición del emisor de partículas.
def cuando_hace_click(evento):
    if evento.x < 100:
        emisor.x = [evento.x], 0.25
        emisor.y = [evento.y], 0.25

pilas.eventos.click_de_mouse.conectar(cuando_hace_click)


# Creando el controlador de propiedades para el emisor.
pc = pilas.actores.Controlador()
pc.x = 230
pc.y = 200

pc.agregar(emisor, 'dy_min', -20, 0)
pc.agregar(emisor, 'dy_max', 0, 20)
pc.agregar_espacio()

pc.agregar(emisor, 'dx_min', -20, 0)
pc.agregar(emisor, 'dx_max', 0, 20)
pc.agregar_espacio()

pc.agregar(emisor, 'escala_min', 0.1, 4)
pc.agregar(emisor, 'escala_max', 0.1, 4)
pc.agregar_espacio()

pc.agregar(emisor, 'rotacion_min', 0, 360)
pc.agregar(emisor, 'rotacion_max', 0, 360)
pc.agregar_espacio()


pilas.avisar(u"Puedes hacer click para cambiar la posición del emisor")
pilas.ejecutar()
