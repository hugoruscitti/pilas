import pilas
pilas.iniciar(usar_motor='qtgl')

fondo = pilas.fondos.DesplazamientoHorizontal()

fondo.agregar("cielo.png", velocidad=0)
fondo.agregar("montes.png", y=100, velocidad=0.5)
fondo.agregar("arboles.png", y=100, velocidad=0.9)
fondo.agregar("pasto.png", y=375, velocidad=2)

p = pilas.actores.Pingu(y=-130)

def cambiar_posicion_camara():
    pilas.escena_actual().camara.x = [p.x], 0.1
    return True

pilas.mundo.agregar_tarea(1/10.0, cambiar_posicion_camara)
pilas.avisar("Utiliza el teclado para mover al personaje.")
pilas.ejecutar()
