# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas

pilas.iniciar()

grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)
mapa = pilas.actores.Mapa(grilla)

mapa.pintar_bloque(10, 10, 0, True)
mapa.pintar_bloque(10, 11, 1, True)
mapa.pintar_bloque(10, 12, 1, True)
mapa.pintar_bloque(10, 13, 1, True)
mapa.pintar_bloque(10, 14, 2, True)


mapa.pintar_bloque(10, 0, 0, True)
mapa.pintar_bloque(10, 1, 1, True)
mapa.pintar_bloque(10, 2, 1, True)
mapa.pintar_bloque(10, 3, 1, True)
mapa.pintar_bloque(10, 4, 2, True)

pelotas = pilas.atajos.fabricar(pilas.actores.Pelota, 10)

pilas.avisar("Creando dos plataformas solidas...")
pilas.ejecutar()
