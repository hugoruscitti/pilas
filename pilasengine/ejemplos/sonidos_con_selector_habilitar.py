import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

un_sonido = pilas.sonidos.cargar("saltar.wav")

def reproducir_sonido():
    un_sonido.reproducir()
    print un_sonido

b = pilas.interfaz.Boton("Reproducir sonido")
b.conectar(reproducir_sonido)

sonido = pilas.actores.Sonido()

pilas.ejecutar()