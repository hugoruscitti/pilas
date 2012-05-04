# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas

def crear_mapa():
    mapa = pilas.actores.Mapa(filas=15, columnas=20)

    mapa.pintar_bloque(10, 6, 0)
    mapa.pintar_bloque(10, 7, 1)
    mapa.pintar_bloque(10, 8, 1)
    mapa.pintar_bloque(10, 9, 1)
    mapa.pintar_bloque(10, 10, 1)
    mapa.pintar_bloque(10, 11, 1)
    mapa.pintar_bloque(10, 12, 2)

    # Pinta todo el suelo
    for columna in range(0, 20):
        mapa.pintar_bloque(14, columna, 1)

    return mapa

pilas.iniciar()

mapa = crear_mapa()
martian = pilas.actores.Martian(mapa)

pilas.avisar("Usa los direccionales para controlar al personaje.")
pilas.ejecutar()

pilas.ejecutar()
