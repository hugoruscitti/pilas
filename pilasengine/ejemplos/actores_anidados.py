import pilasengine

pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.x = [100], 10
aceituna = pilas.actores.Aceituna()

#aceituna_grande = pilas.actores.Aceituna()
#aceituna_grande.x = 100
#aceituna_grande.escala = 0.75

aceituna.agregar(mono)
aceituna.rotacion = [180], 10

pilas.ejecutar()