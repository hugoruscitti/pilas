import pilas

pilas.iniciar(usar_motor='qt')

p = pilas.actores.Pelota() * 3

pilas.avisar("Usando el motor Qt (sin opengl)")
pilas.ejecutar()
