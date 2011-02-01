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

        if control.izquierda:
            self.figura.x -= 5
            self.espejado = True
        elif control.derecha:
            self.figura.x += 5
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


    pilas.ejecutar()
