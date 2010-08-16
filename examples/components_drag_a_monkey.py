import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.components.Draggable)

pilas.loop()
