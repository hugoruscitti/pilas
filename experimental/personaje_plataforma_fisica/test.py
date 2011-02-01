import pilas


class Personaje(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self, 'data/personaje.png')
        self.centro = ("centro", 70)

        self.figura = pilas.fisica.Circulo(0, 0, 20, friccion=0)
        self.saltando = False

    def actualizar(self):
        self.x = self.figura.x 
        self.y = self.figura.y
        control = pilas.mundo.control

        # Obtiene la velocidad en x e y para luego
        # realizar movimiento en x, sin alterar
        x, y = self.figura._cuerpo.GetLinearVelocity()
        self.figura.empujar(x/2, y)


        if control.izquierda:
            self.figura.empujar(-100, y)
            self.espejado = True
        elif control.derecha:
            self.figura.empujar(+100, y)
            self.espejado = False

        # TODO: Evitar que salte muchas veces, por ejemplo
        #       si se deja pulsado hacia arriba...
        #       (el problema es que no se la condicion para dejar de saltar...)
        if control.arriba:
            self.figura.empujar(0, 1000)
            self.saltando = True


if __name__ == '__main__':
    pilas.iniciar()
    personaje = Personaje()


    # Un Mapa
    grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)
    mapa = pilas.actores.Mapa(grilla)

    mapa.pintar_bloque(10, 10, 0)
    mapa.pintar_bloque(10, 11, 1)
    mapa.pintar_bloque(10, 12, 1)
    mapa.pintar_bloque(10, 13, 1)
    mapa.pintar_bloque(10, 14, 2)

    # Cajas que molestan..
    pilas.atajos.fabricar(pilas.actores.Caja, 10)

    pilas.actores.Pelota()
    pilas.actores.Pelota()



    # Suelo en diagonal
    rectangulo = pilas.fisica.Rectangulo(0, 0, 290/2, 20/2, dinamica=False)
    rectangulo.rotacion = 40
    suelo_inclinado= pilas.actores.Actor("data/suelo.png")
    suelo_inclinado.aprender(pilas.habilidades.Imitar, rectangulo)



    pilas.ejecutar()
