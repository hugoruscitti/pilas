import pilasengine

pilas = pilasengine.iniciar()

pilas.fondos.Cesped()
shaolin = pilas.actores.Shaolin(y=-100)

pilas.ejecutar()
