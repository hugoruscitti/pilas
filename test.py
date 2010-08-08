import pilas

actor = pilas.actors.Actor("doc/source/images/lgplv3.png")
mono = pilas.actors.Monkey()
mono.x = 100
mono.scale = 2
mono.rotation = 0
pilas.loop()
