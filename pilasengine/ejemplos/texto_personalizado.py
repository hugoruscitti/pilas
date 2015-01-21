import pilasengine

pilas = pilasengine.iniciar()
texto_personalizado = pilas.actores.Texto("Hola ?", magnitud=70, fuente="visitor1.ttf", y=100)
pilas.ejecutar()
