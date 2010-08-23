import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.comportamientos.MovedByKeyboard)


pilas.bucle()
