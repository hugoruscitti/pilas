import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)

pilas.depurador.definir_modos(fisica=True)

#mono = pilas.actores.Mono()
p = pilas.actores.Pelota() * 10
#b = pilas.fisica.Rectangulo(0,0, 100,100, dinamica=False)
#p.definir_figura_de_colision(b)

#p.impulsar(1,0)


pilas.fisica.Rectangulo(0, -100, 100, 100, dinamica=False)

pilas.ejecutar()