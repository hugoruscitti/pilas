import pilas

def test_posicion_de_los_actores():
    pilas.iniciar()
    mono = pilas.actores.Mono()

    # el actor comienza en el centro de la ventana
    assert mono.x == 0
    assert mono.y == 0

    # un cambio de posicion sencillo
    mono.x = 100
    mono.y = 100
    assert mono.x == 100
    assert mono.y == 100

    # rotacion
    assert mono.rotacion == 0

    mono.rotacion = 180
    assert mono.rotacion == 180

    # Verificnado que las rotaciones siempre estan entre 0 y 360
    mono.rotacion = 361
    assert mono.rotacion == 1

    mono.rotacion = -10
    assert mono.rotacion == 350

    # Analizando el actor existira en la escena
    assert mono in pilas.escena_actual().actores

    # Escalas
    assert mono.escala == 1

    mono.escala = 0
    assert mono.escala == 0.001

    mono.escala = 0.5
    assert mono.escala == 0.5

    mono.escala = 5
    assert mono.escala == 5

    # verificando que el mono se elimina de la escena.
    mono.eliminar()
    assert not (mono in pilas.escena_actual().actores)


def test_correlacion_de_posiciones():
    mono = pilas.actores.Mono()

    assert mono.x == 0
    assert mono.y == 0

    mono.izquierda = mono.izquierda - 100
    assert mono.x == -100

    mono.derecha = mono.derecha + 100
    assert mono.x == 0

    mono.arriba = mono.arriba + 100
    assert mono.y == 100

    mono.abajo = mono.abajo - 100
    assert mono.y == 0

    mono.eliminar()

def test_colisiones_contra_un_punto():
    mono = pilas.actores.Mono()
    assert mono.colisiona_con_un_punto(0, 0)
    assert not mono.colisiona_con_un_punto(200, 200)
