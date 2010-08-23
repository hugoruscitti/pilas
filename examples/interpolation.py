import pilas

mono = pilas.actors.Monkey()
mono.x = 0
mono.y = 0
mono.rotation = pilas.interpolar(360, duration=3)
mono.scale = pilas.interpolar(2, duration=3)
mono.x = pilas.interpolar(320, duration=3)
mono.y = pilas.interpolar(240, duration=3)


# Formar un cuadrado
#mono.x = 100
#mono.y = 100
#mono.x = pilas.interpolar(400, 400, 100, 100, duration=3)
#mono.y = pilas.interpolar(100, 400, 400, 100, duration=4)


pilas.bucle()
