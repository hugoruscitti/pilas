import pilas

def test_reemplazar_fondo():
    pilas.iniciar()
    # se asegura de que solo exite un fondo.
    fondos = [x for x in pilas.escena_actual().actores if x.es_fondo()]
    assert len(fondos) == 1

    # y al crear un nuevo fondo se asegura de que sigue existiendo solo uno.
    pilas.fondos.Espacio()
    fondos = [x for x in pilas.escena_actual().actores if x.es_fondo()]
    assert len(fondos) == 1
