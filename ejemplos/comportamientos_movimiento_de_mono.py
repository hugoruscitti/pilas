import pilas

pilas.iniciar()
mono = pilas.actores.Mono()

pasos = 100

mono.x = -50
mono.y = -50

mono.hacer(pilas.comportamientos.Avanzar(0, pasos), True)
mono.hacer(pilas.comportamientos.Avanzar(90, pasos), True)
mono.hacer(pilas.comportamientos.Avanzar(180, pasos), True)
mono.hacer(pilas.comportamientos.Girar(360, 10), True)
mono.hacer(pilas.comportamientos.Avanzar(270, pasos), True)

pilas.avisar("Movimiento mediante comportamientos.")
pilas.ejecutar()
