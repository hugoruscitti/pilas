import pilas

mono = pilas.actors.Monkey()
mono.scale = 1
mono.rotation = 0

def girar():
    mono.rotation = mono.rotation + 1
    return True

pilas.add_task(0, girar)

pilas.loop()
