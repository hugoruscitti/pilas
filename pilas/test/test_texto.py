import pilas

def test_posicion_de_los_actores():
    pilas.iniciar()
    texto = pilas.actores.Texto('Hola')
    assert texto.texto == 'Hola'
    assert texto.obtener_texto() == "Hola"
