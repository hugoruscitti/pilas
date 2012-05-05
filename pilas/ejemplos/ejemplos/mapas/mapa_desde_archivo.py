import pilas
pilas.iniciar(gravedad=(0,0))
mapa = pilas.actores.MapaTiled('parque.tmx')

# Genera un personaje en movimiento.
aceituna = pilas.actores.Aceituna()
aceituna.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.avisar("Use el teclado para mover al personaje.")
pilas.ejecutar()
