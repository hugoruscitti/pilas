import pilas
pilas.iniciar()
b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b,1)
r.forward(50,3)
pilas.ejecutar()
