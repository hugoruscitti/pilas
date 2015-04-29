import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

# El primer mono tiene una figura con restitucion
texto1 = pilas.actores.Texto("Con restitucion", x=-100)
c1 = pilas.fisica.Circulo(-100, 0, 50, restitucion=1, amortiguacion=1)
b1 = pilas.actores.Mono()
b1.imitar(c1)
b1.aprender('arrastrable')


# El primer mono tiene una figura con restitucion
texto2 = pilas.actores.Texto("Sin restitucion", x=100)
c2 = pilas.fisica.Circulo(100, 0, 50, restitucion=0.1, amortiguacion=1)
b2 = pilas.actores.Mono()
b2.imitar(c2)
b2.aprender('arrastrable')


pilas.avisar("Efecto de restituciones, usa el mouse para arrastrar...")
pilas.ejecutar()

