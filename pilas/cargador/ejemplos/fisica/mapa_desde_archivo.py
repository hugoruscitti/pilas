import pilas
pilas.iniciar(gravedad=(0,0))
mapa = pilas.actores.Mapa('parque.tmx')

# Genera un personaje en movimiento.
aceituna = pilas.actores.Aceituna()
circulo = pilas.fisica.Circulo(0, 0, 14, restitucion=1, friccion=0)
aceituna.imitar(circulo)
circulo.impulsar(20000, 20000)

pilas.avisar("Cargando el mapa desde un archivo (F11 muestra colisiones)")
pilas.ejecutar()
