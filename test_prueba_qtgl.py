import pilas

pilas.iniciar(usar_motor='qtgl')

p = pilas.actores.Pelota() * 3

pilas.avisar("Usando el motor QtGL")
pilas.ejecutar()
