import pilasengine

pilas = pilasengine.iniciar()

mapa = pilas.actores.MapaTiled('mapa_desde_archivo.tmx')

# Genera un personaje en movimiento.
maton = pilas.actores.Maton()


pilas.avisar("Use el teclado para mover al personaje.")

pilas.ejecutar()
