# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas

def crear_mapa():
    mapa = pilas.actores.Mapa(filas=15, columnas=20)

    # Plataforma superior (la que esta en medio de la pantalla)
    mapa.pintar_bloque(9, 6, 0)
    mapa.pintar_bloque(9, 7, 1)
    mapa.pintar_bloque(9, 8, 1)
    mapa.pintar_bloque(9, 9, 1)
    mapa.pintar_bloque(9, 10, 1)
    mapa.pintar_bloque(9, 11, 1)
    mapa.pintar_bloque(9, 12, 2)

    # Plataforma pequeña, mas abajo que la anterior.
    mapa.pintar_bloque(12, 12, 0)
    mapa.pintar_bloque(12, 13, 1)
    mapa.pintar_bloque(12, 14, 1)
    mapa.pintar_bloque(12, 15, 2)

    mapa.pintar_bloque(13, 12, 8, False)
    mapa.pintar_bloque(13, 13, 9, False)
    mapa.pintar_bloque(13, 14, 9, False)
    mapa.pintar_bloque(13, 15, 10, False)

    mapa.pintar_bloque(13, 0, 7, True)
    mapa.pintar_bloque(12, 0, 7, True)
    mapa.pintar_bloque(11, 0, 7, True)
    mapa.pintar_bloque(10, 0, 7, True)

    mapa.pintar_bloque(13, 19, 7, True)
    mapa.pintar_bloque(12, 19, 7, True)
    mapa.pintar_bloque(11, 19, 7, True)
    mapa.pintar_bloque(10, 19, 7, True)

    # Pinta todo el suelo
    for columna in range(0, 20):
        mapa.pintar_bloque(14, columna, 1)

    return mapa

pilas.iniciar()

mapa = crear_mapa()
martian = pilas.actores.Martian(mapa)
martian.aprender(pilas.habilidades.SiempreEnElCentro)

pilas.avisar("Usa los direccionales para controlar al personaje.")
pilas.ejecutar()

pilas.ejecutar()
