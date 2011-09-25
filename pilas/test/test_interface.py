import pilas

def test_todos_los_objetos_de_interfaz_se_pueden_crear():
    pilas.iniciar()

    deslizador = pilas.interfaz.Deslizador()
    assert deslizador
    assert deslizador.progreso == 0

    boton = pilas.interfaz.Boton()
    assert boton

    ingreso = pilas.interfaz.IngresoDeTexto()
    assert ingreso

    try:
        pilas.interfaz.ListaSeleccion()
    except TypeError:
        assert True   # Se espera esta excepcion, porque un argumento es obligatorio

    lista = pilas.interfaz.ListaSeleccion([('uno')])
    assert lista

    try:
        pilas.interfaz.Selector()
    except TypeError:
        assert True   # el argumento texto es obligatorio.

    selector = pilas.interfaz.Selector("hola")
    assert selector
