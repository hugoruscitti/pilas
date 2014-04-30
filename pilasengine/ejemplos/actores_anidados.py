import pilasengine


pilas = pilasengine.iniciar()

aceituna = pilas.actores.Aceituna()
aceituna2 = pilas.actores.Aceituna()
aceituna2.x = 100

aceituna.agregar(aceituna2)
aceituna.rotacion = [180]

pilas.ejecutar()