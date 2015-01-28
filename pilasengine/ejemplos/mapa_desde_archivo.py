import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
mapa = pilas.actores.MapaTiled('mapa.tmx')

# Genera un personaje en movimiento.
#maton = pilas.actores.personajes_rpg.Maton(mapa)

pilas.avisar("Use el teclado para mover al personaje.")

pilas.ejecutar()
