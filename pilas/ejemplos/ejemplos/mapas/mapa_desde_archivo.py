import pilas
pilas.iniciar(gravedad=(0,0))
mapa = pilas.actores.MapaTiled('mapa.tmx')

# Genera un personaje en movimiento.
aceituna = pilas.actores.personajes_rpg.Maton(mapa)

pilas.avisar("Use el teclado para mover al personaje.")

pilas.ejecutar()
