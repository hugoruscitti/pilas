import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(fisica=True)


mono = pilas.actores.Mono(200, 0)

f = pilas.fisica.Circulo(0, 0, 50, dinamica=True, sensor=True)
mono.definir_colision(f)

mono.aprender(pilas.habilidades.Arrastrable)
mono.aprender(pilas.habilidades.MoverseConElTeclado)


banana = pilas.actores.Banana(0, 0)

f = pilas.fisica.Circulo(0, 0, 30, dinamica=True, sensor=True)
banana.definir_colision(f)

pelota = pilas.actores.Pelota(y=200) * 3
#pelota.figura.sensor = True

def colisionan(m, b):
    print m, b

def colisiona_con_pelota(m, b):
    print "Colisiona con una pelota"
    print m, b
    b.eliminar()

pilas.colisiones.agregar(mono, banana, colisionan)
pilas.colisiones.agregar(mono, pelota, colisiona_con_pelota)


pilas.ejecutar()
