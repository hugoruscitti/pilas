import pilas

def test_mapa_y_distancia_al_suelo():
    pilas.iniciar()
    mapa = pilas.actores.Mapa(filas=14, columnas=14)
    mapa.pintar_bloque(13, 9, 1, True)
    mapa.pintar_bloque(13, 10, 1, True)

    # Me aseguro de que el mapa interpreta correctamente
    # cuales de los bloques son solidos.
    assert mapa.es_punto_solido(80, -210)
    assert not mapa.es_punto_solido(0, 0)

    # Me aseguro de calcular la distancia al suelo correctamente
    assert mapa.obtener_distancia_al_suelo(80, -100, 200) == 92

    # Si no hay suelo en toda la columna, se tiene que retornar
    # el limite maximo
    assert mapa.obtener_distancia_al_suelo(0, 0, 2000) == 2000

    # Me aseguro, que que el mapa responde a cuales
    # son los bloques solidos aunque cambie la posicion del
    # mapa entero..
    mapa.x = 200
    mapa.y = 200

    assert mapa.es_punto_solido(80+200, -210+200)
    assert not mapa.es_punto_solido(0+200, 0+200)
    mapa.x = 0
    mapa.y = 0
    mapa.pintar_limite_de_bloques()
