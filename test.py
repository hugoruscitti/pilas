import pilas

actor = pilas.actors.Actor("doc/source/images/lgplv3.png")
mono = pilas.actors.Monkey()
mono.x = 100
mono.scale = 2
mono.rotation = 0

mono.smile()

def girar():
    x = mono.rotation
    x += 1
    mono.rotation = x
    return True

pilas.add_task(0, girar)

pilas.loop()
