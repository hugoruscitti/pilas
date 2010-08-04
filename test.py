import pilas

actor = pilas.actors.Actor("doc/source/images/lgplv3.png")
mono = pilas.actors.Monkey()
mono.x = 10
mono.rotation = 10
pilas.loop()
