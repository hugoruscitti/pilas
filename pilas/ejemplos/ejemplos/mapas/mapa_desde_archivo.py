import pilas
pilas.iniciar(gravedad=(0,0))
mapa = pilas.actores.MapaTiled('parque.tmx')

# Genera un personaje en movimiento.
aceituna = pilas.actores.personajes_rpg.Maton()

pilas.avisar("Use el teclado para mover al personaje.")

pilas.ejecutar()
