import pilas

mono = pilas.actors.Monkey()
elastic = pilas.pytweener.Easing.Elastic.easeInOut
#lineal = pilas.pytweener.Easing.Linear.easeNone

# Rotacion
pilas.tweener.addTween(mono, SetRotation=360, tweenTime=5000, tweenType=elastic)

# Escalado
pilas.tweener.addTween(mono, SetScaleX=3, tweenTime=5000, tweenType=elastic)
pilas.tweener.addTween(mono, SetScaleY=3, tweenTime=5500, tweenType=elastic)


pilas.loop()
