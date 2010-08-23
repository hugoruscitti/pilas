import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.comportamientos.FollowMouseClicks)
mono.mixin(pilas.comportamientos.SizeByWheel)

pilas.bucle()
