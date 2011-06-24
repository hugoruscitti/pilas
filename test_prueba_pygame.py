import pilas

pilas.iniciar(usar_motor='pygame')

p = pilas.actores.Pelota() * 3

pilas.avisar("Usando el motor pygame")
pilas.ejecutar()
