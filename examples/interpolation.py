import pilas

mono = pilas.actors.Monkey()
mono.x = 0
mono.y = 0
mono.rotation = pilas.interpolate(0, 360, duration=3)
mono.scale = pilas.interpolate(0, 2, duration=3)
mono.x = pilas.interpolate(0, 320, duration=3)
mono.y = pilas.interpolate(0, 240, duration=3)

#elastic = pilas.pytweener.Easing.Elastic.easeInOut
#lineal = pilas.pytweener.Easing.Linear.easeNone

# Rotacion
#pilas.tweener.addTween(mono, SetRotation=360, tweenTime=5000, tweenType=elastic)

# Escalado
#pilas.tweener.addTween(mono, SetScaleX=3, tweenTime=5000, tweenType=elastic)
#pilas.tweener.addTween(mono, SetScaleY=3, tweenTime=5500, tweenType=elastic)

pilas.loop()
