import pilas

mono = pilas.actores.Mono()
mono.x = 0
mono.y = 0
mono.rotacion = pilas.interpolar(360, duration=3)
mono.escala = pilas.interpolar(2, duration=3)
mono.x = pilas.interpolar(320, duration=3)
mono.y = pilas.interpolar(240, duration=3)

pilas.avisar("Un ejemplo de interpolacion en dos dimensiones.")
pilas.ejecutar()

