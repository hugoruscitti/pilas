import pilas

pilas.iniciar()

grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)
mapa = pilas.actores.Mapa(grilla)

mapa.pintar_bloque(2, 10, 0, True)
mapa.pintar_bloque(2, 11, 1, True)
mapa.pintar_bloque(2, 12, 1, True)
mapa.pintar_bloque(2, 13, 1, True)
mapa.pintar_bloque(2, 14, 2, True)


mapa.pintar_bloque(2, 0, 0, True)
mapa.pintar_bloque(2, 1, 1, True)
mapa.pintar_bloque(2, 2, 1, True)
mapa.pintar_bloque(2, 3, 1, True)
mapa.pintar_bloque(2, 4, 2, True)

pelotas = pilas.atajos.fabricar(pilas.actores.Pelota, 10)

pilas.avisar("Creando dos plataformas solidas...")
pilas.ejecutar()

