import pilas

mono = pilas.actors.Monkey()

def mover_al_mono(sender, x, y, signal):
    mono.x = x
    mono.y = y

pilas.signals.mouse_move.connect(mover_al_mono)

pilas.loop()
