import pilasengine

pilas = pilasengine.iniciar()

fondo = pilas.fondos.DesplazamientoHorizontal()

fondo.agregar("cielo.png", velocidad=0)
fondo.agregar("montes.png", y=100, velocidad=0.5)
fondo.agregar("arboles.png", y=100, velocidad=0.9)
fondo.agregar("pasto.png", y=375, velocidad=2)

p = pilas.actores.Pingu(y=-180)

def cambiar_posicion_camara():
    pilas.camara.x += (p.x - pilas.camara.x) / 20.0
    return True

pilas.tareas.agregar(1/40.0, cambiar_posicion_camara)
pilas.avisar("Utiliza el teclado para mover al personaje.")
pilas.ejecutar()
