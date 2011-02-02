import pilas


class Personaje(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self, 'data/personaje.png')
        
        self.centro = ("centro", 70)
        self.figura = pilas.fisica.Circulo(100, 200, 20, restitucion=0)
        self.saltando = False
        self.solto_control_arriba = False
        self.bajando = True

    def actualizar(self):
        self.x = self.figura.x 
        self.y = self.figura.y
        control = pilas.mundo.control
        self.figura._cuerpo.WakeUp()
        # Obtiene la velocidad en x e y para luego
        # realizar movimiento en x, sin alterar
        
        x, y = self.figura.obtener_velocidad_lineal()
        self.figura.definir_velocidad_lineal(x/2, y)

        if control.izquierda:
            self.figura.definir_velocidad_lineal(-100, y)
            self.espejado = True
        elif control.derecha:
            self.figura.definir_velocidad_lineal(+100, y)
            self.espejado = False

        
        self.estable = (-20 < y < 20)
        
        if not self.estable:
            if y < -20:
                self.bajando = True
            elif y > 20:
                self.bajando = False

        # TODO: Evitar que salte muchas veces, por ejemplo
        #       si se deja pulsado hacia arriba...
        #       (el problema es que no se la condicion para dejar de saltar...)
        if control.arriba:
            if self.solto_control_arriba and self.toca_el_suelo():
                self.figura.definir_velocidad_lineal(0, 140)
                self.solto_control_arriba = False
                print "Comienza a saltar"
        else:
            self.solto_control_arriba = True

    def toca_el_suelo(self):
        return self.estable and self.bajando

if __name__ == '__main__':
    pilas.iniciar()
    personaje = Personaje()

    # Elimino el suelo y las paredes para crearlas
    # nuevamente con menos restitucion
    pilas.mundo.fisica.eliminar_suelo()
    pilas.mundo.fisica.eliminar_paredes()

    pilas.mundo.fisica.crear_suelo(restitucion=0)
    pilas.mundo.fisica.crear_paredes(restitucion=0)

    
    # Un Mapa
    grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)
    mapa = pilas.actores.Mapa(grilla, restitucion=0)

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
    rectangulo = pilas.fisica.Rectangulo(0, 0, 290, 20, dinamica=False, restitucion=0)
    rectangulo.rotacion = 40
    suelo_inclinado= pilas.actores.Actor("data/suelo.png")
    suelo_inclinado.aprender(pilas.habilidades.Imitar, rectangulo)
    
    pilas.ejecutar()
