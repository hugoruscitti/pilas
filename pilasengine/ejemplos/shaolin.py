import pilasengine

pilas = pilasengine.iniciar()

pilas.fondos.Cesped()
shaolin = pilas.actores.Shaolin(y=-100)

pilas.avisar("Pulsa el teclado para manejar al shaolin")
pilas.ejecutar()
