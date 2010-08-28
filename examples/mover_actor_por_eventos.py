import pilas

mono = pilas.actores.Mono()

def mover_al_mono(sender, x, y, signal):
    mono.x = x
    mono.y = y

pilas.eventos.mueve_mouse.connect(mover_al_mono)

pilas.ejecutar()
