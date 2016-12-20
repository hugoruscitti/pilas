import pilas

def test_perseguir():
    pilas.iniciar()

    # se asegura que persigue bien en las cuatro direcciones
    mono = pilas.actores.Mono()
    mono.x = 100
    mono.y = 100
    bomba = pilas.actores.Bomba()
    bomba.aprender(pilas.habilidades.PerseguirAOtroActor, mono)

    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x > 0
    assert bomba.y > 0

    bomba.x = 0
    bomba.y = 0
    mono.x = 100
    mono.y = -100

    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x > 0
    assert bomba.y < 0

    bomba.x = 0
    bomba.y = 0
    mono.x = -100
    mono.y = 100

    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x < 0
    assert bomba.y > 0
    
    bomba.x = 0
    bomba.y = 0
    mono.x = -100
    mono.y = -100

    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x < 0
    assert bomba.y < 0

    # se asegura que la velocidad funciona como tiene que funcionar
    
    mono.x = 100
    mono.y = 100
    bomba.x = 0
    bomba.y = 0
    
    bomba.habilidades.habilidades[1].velocidad = 1
    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x == 1
    assert bomba.y == 1

    bomba.x = 0
    bomba.y = 0
    
    bomba.habilidades.habilidades[1].velocidad = 5
    bomba.habilidades.habilidades[1].actualizar()
    assert bomba.x == 5
    assert bomba.y == 5

    # se asegura que cuando es menos inteligente tarda mas en atrapar

    bomba.x = 0
    bomba.y = 0
    
    bomba.habilidades.habilidades[1].velocidad = 1

    contador_inteligente = 0
    while bomba.x != mono.x and bomba.y != mono.y:
        bomba.habilidades.habilidades[1].actualizar()
        contador_inteligente += 1

    bomba.x = 0
    bomba.y = 0
    
    bomba.habilidades.habilidades[1].velocidad = 1
    bomba.habilidades.habilidades[1].inteligencia = 0

    contador_perdido = 0
    while bomba.x != mono.x and bomba.y != mono.y:
        bomba.habilidades.habilidades[1].actualizar()
        contador_perdido += 1
    
    assert contador_inteligente > contador_perdido

