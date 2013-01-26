import pilas

pilas.iniciar()

a = pilas.actores.Texto("Hola?")
a.y = [-120]

b = pilas.actores.Texto("Hola?", magnitud=70, fuente="../gamejam2013/data/visitor1.ttf", y=100)

pilas.ejecutar()
