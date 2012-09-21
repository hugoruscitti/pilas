import pilas
pilas.iniciar(usar_motor='qtgl')

cielo = pilas.actores.Actor("cielo.png")
montes = pilas.actores.Actor("montes.png")
arboles = pilas.actores.Actor("arboles.png")
pasto = pilas.actores.Actor("pasto.png", y=-179)

cielo.z = 10
montes.z = 5
arboles.z = 0
pasto.z = -10

fondo = pilas.fondos.Desplazamiento()

fondo.agregar(cielo, 0)
fondo.agregar(montes, 0.5)
fondo.agregar(arboles, 0.9)
fondo.agregar(pasto, 2)

pilas.escena_actual().camara.x = [200], 10

pilas.ejecutar()
