import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)

pilas.depurador.definir_modos(fisica=True)

mono = pilas.actores.Mono()

#figura = pilas.fisica.Rectangulo(0, 0, 30, 30, dinamica=False, sensor=True)

mono.definir_colision(figura)

caja = pilas.fisica.Rectangulo(0, 200, 50, 50)

mono.aprender(pilas.habilidades.MoverseConElTeclado)

bananas = pilas.actores.Banana() * 30

def comer(m, b):
    b.eliminar()

pilas.colisiones.agregar(mono, bananas, comer)



#def saludar():
#    print "hola?"

#def disparar_mono():
#    m = pilas.actores.Mono()
#    m.x = [200]

#b = pilas.actores.Menu([
#                        ("saludar", saludar),
#                        ("disparar", disparar_mono)
#                        ])

pilas.ejecutar()