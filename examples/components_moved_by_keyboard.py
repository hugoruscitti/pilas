import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.components.MovedByKeyboard)


pilas.loop()
