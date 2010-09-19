import pilas

pilas.iniciar()

tortuga = pilas.actores.Tortuga()
tortuga.girar(45)
tortuga.avanzar(100)

pilas.camara.x = pilas.interpolar(200, 0)

pilas.avisar("Moviendo la camara...")
pilas.ejecutar()
