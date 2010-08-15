import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.components.FollowMouseClicks)
mono.mixin(pilas.components.SizeByWheel)

pilas.loop()
