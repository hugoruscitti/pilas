import pilas

def test_posiciones_de_los_actores():
    pilas.iniciar()

    caja = pilas.actores.Actor("caja.png")

    #  +------------+
    #  |            |
    #  |            |
    #  |      x     |
    #  |            |
    #  |            |
    #  +------------+

    assert caja.alto == 48
    assert caja.ancho == 48

    assert caja.arriba == 24
    assert caja.abajo == -24
    assert caja.izquierda == -24
    assert caja.derecha == 24


def test_escala_reducida():
    pilas.iniciar()
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 0.5                           
    
    #  +------------+   # La caja resultado
    #  |            |   # es la interior.
    #  |   +----+   |
    #  |   |    |   |
    #  |   +----+   |
    #  |            |
    #  +------------+

    assert caja.alto == 24
    assert caja.ancho == 24

    assert caja.x == 0
    assert caja.y == 0

    assert caja.arriba == 12
    assert caja.abajo == -12
    assert caja.izquierda == -12
    assert caja.derecha == 12

def test_escala_ampliada():
    pilas.iniciar()
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 2

    assert caja.alto == 48*2
    assert caja.ancho == 48*2

    assert caja.x == 0
    assert caja.y == 0

    assert caja.arriba == 48
    assert caja.abajo == -48
    assert caja.izquierda == -48
    assert caja.derecha == 48


def test_cambio_horizontal_de_centro():
    pilas.iniciar()
    caja = pilas.actores.Actor("caja.png")      
    caja.escala = 1
    caja.centro = ("izquierda", "centro")
    #  +------------+
    #  |            |
    #  |            |
    #  |x           |
    #  |            |
    #  |            |
    #  +------------+
    
    assert caja.alto == 48
    assert caja.ancho == 48

    assert caja.arriba == 24
    assert caja.abajo == -24
    assert caja.izquierda == 0
    assert caja.derecha == 48

    caja.centro = ("derecha", "centro")
    #  +------------+
    #  |            |
    #  |            |
    #  |           x|
    #  |            |
    #  |            |
    #  +------------+

    assert caja.arriba == 24
    assert caja.abajo == -24
    assert caja.izquierda == -48
    assert caja.derecha == 0


def test_cambiocentrovertical():
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 1
    caja.centro = ("centro", "arriba")
    #  +------------+
    #  |      x     |
    #  |            |
    #  |            |
    #  |            |
    #  |            |
    #  +------------+

    assert caja.alto == 48
    assert caja.ancho == 48

    assert caja.abajo == -48
    assert caja.arriba == 0

    assert caja.izquierda == -24
    assert caja.derecha == 24

    caja.centro = ("centro", "abajo")
    #  +------------+
    #  |            |
    #  |            |
    #  |            |
    #  |            |
    #  |      x     |
    #  +------------+

    assert caja.arriba == 48
    assert caja.abajo == 0
    assert caja.izquierda == -24
    assert caja.derecha == 24

def test_cambiocentroverticalyhorizontalnocentrado():
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 1

    caja.centro = (10, 10)

    #  +------------+
    #  |            |
    #  |   x        |
    #  |            |
    #  |            |
    #  |            |
    #  +------------+

    assert caja.alto == 48
    assert caja.ancho == 48

    assert caja.abajo == -38
    assert caja.arriba == 10

    assert caja.izquierda == -10
    assert caja.derecha == 38

def test_cambiocentroverticalyhorizontalnocentradoconreducciondeescala():
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 0.5

    caja.centro = (10, 10)

    #  +------------+
    #  |            |
    #  |   x        |
    #  |            |
    #  |            |
    #  |            |
    #  +------------+

    assert caja.alto == 24
    assert caja.ancho == 24

    assert caja.abajo == -38/2
    assert caja.arriba == 5

    assert caja.izquierda == -5
    assert caja.derecha == 38/2

def test_cambiodeposicionhorizontalconescala():
    caja = pilas.actores.Actor("caja.png")
    caja.escala = 1

    assert caja.izquierda == -24
    assert caja.derecha == 24

    # Prueba dos cambios que no tendrian que afectar
    caja.izquierda = -24
    assert caja.izquierda == -24
    assert caja.derecha == 24

    caja.derecha = 24
    assert caja.izquierda == -24
    assert caja.derecha == 24

    caja.escala = 0.5

    assert caja.izquierda == -12
    assert caja.derecha == 12

    # Prueba dos cambios que no tendrian que afectar
    caja.izquierda = -20
    assert caja.izquierda == -20
    assert caja.derecha == -20 + 24

    caja.derecha = 0
    assert caja.izquierda == -24
    assert caja.derecha == 0

def test_cambiodeposicionverticalconescala():
    caja = pilas.actores.Actor("caja.png")
    caja.centro = ("centro", "centro")
    caja.escala = 1

    assert caja.area == 48
    assert caja.arriba == 24
    assert caja.abajo == -24

    caja.arriba = 0
    assert caja.arriba == 0
    assert caja.abajo == -48

    caja.abajo = 0
    assert caja.arriba == 48
    assert caja.abajo == 0


    caja.escala = 0.5
    assert caja.area, (24 == 24)
    caja.x, caja.y = (0, 0)

    assert caja.arriba == 12
    assert caja.abajo == -12

    # Prueba dos cambios que no tendrian que afectar
    caja.izquierda = -20
    assert caja.izquierda == -20
    assert caja.derecha == -20 + 24

    caja.derecha = 0
    assert caja.izquierda == -24
    assert caja.derecha == 0

