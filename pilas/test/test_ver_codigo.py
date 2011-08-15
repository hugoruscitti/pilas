import pilas

def test_ver_codigo():
    pilas.iniciar()
    assert pilas.ver(pilas, False, True)
    assert pilas.ver(pilas.habilidades, False, True)
    assert pilas.ver(pilas.habilidades.Arrastrable, False, True)
