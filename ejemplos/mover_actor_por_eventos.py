import pilas

mono = pilas.actores.Mono()

def mover_al_mono(sender, x, y, signal, dx, dy):
    mono.x = x
    mono.y = y

pilas.eventos.mueve_mouse.connect(mover_al_mono)

pilas.avisar("Moviendo un actor en base a la posicion del mouse.")
pilas.ejecutar()
