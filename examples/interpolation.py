import pilas

mono = pilas.actors.Monkey()
mono.x = 0
mono.y = 0
mono.rotation = pilas.interpolate(360, duration=3)
mono.scale = pilas.interpolate(2, duration=3)
mono.x = pilas.interpolate(320, duration=3)
mono.y = pilas.interpolate(240, duration=3)


# Formar un cuadrado
#mono.x = 100
#mono.y = 100
#mono.x = pilas.interpolate(400, 400, 100, 100, duration=3)
#mono.y = pilas.interpolate(100, 400, 400, 100, duration=4)


pilas.loop()
