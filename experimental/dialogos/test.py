import pilas

class Globo(pilas.actores.Actor):
    
    def __init__(self, texto, x=0, y=0):
        pilas.actores.Actor.__init__(self)
        ancho, alto, tamano = self._crear_lienzo(texto, pilas) 
        imagen = pilas.imagenes.cargar_imagen_cairo("globo.png")


        self._pintar_globo(x, y, ancho, alto, imagen)
        
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(texto, 12, 25, tamano=14)
        self.lienzo.asignar(self)
        self.centro = ("derecha", "abajo")

    def _crear_lienzo(self, texto, pilas):
        self.lienzo = pilas.lienzo.Lienzo(10, 10)
        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)
        ancho = int((ancho + 12) - (ancho % 12))
        alto = int((alto + 12) - alto % 12)
        self.lienzo = pilas.lienzo.Lienzo(ancho + 36, alto + 24 + 35)
        return ancho, alto, tamano

    def _pintar_globo(self, x, y, ancho, alto, imagen):
        # esquina sup-izq
        self.lienzo.pintar_parte_de_imagen(imagen, 0, 0, 12, 12, 0, 0)
    # borde superior
        for x in range(0, int(ancho) + 12, 12):
            self.lienzo.pintar_parte_de_imagen(imagen, 12, 0, 12, 12, 12 + x, 0)
        
    # esquina sup-der
        self.lienzo.pintar_parte_de_imagen(imagen, 100, 0, 12, 12, 12 + int(ancho) + 12, 0)
    # centro del dialogo
        for y in range(0, int(alto) + 12, 12):
            # borde izquierdo
            self.lienzo.pintar_parte_de_imagen(imagen, 0, 12, 12, 12, 0, 12 + y)
            # linea horizontal blanca, para el centro del dialogo.
            for x in range(0, int(ancho) + 12, 12):
                self.lienzo.pintar_parte_de_imagen(imagen, 12, 12, 12, 12, 12 + x, 12 + y)
            
            # borde derecho
            self.lienzo.pintar_parte_de_imagen(imagen, 100, 12, 12, 12, 12 + int(ancho) + 12, 12 + y)
        
    # parte inferior
        self.lienzo.pintar_parte_de_imagen(imagen, 0, 35, 12, 12, 0, 0 + int(alto) + 12 + 12)
    # linea horizontal de la parte inferior
        for x in range(0, int(ancho) + 12, 12):
            self.lienzo.pintar_parte_de_imagen(imagen, 12, 35, 12, 12, 12 + x, 0 + int(alto) + 12 + 12)
        
        self.lienzo.pintar_parte_de_imagen(imagen, 100, 35, 12, 12, 12 + int(ancho) + 12, 0 + int(alto) + 12 + 12)
    # Pico de la parte de abajo
        self.lienzo.pintar_parte_de_imagen(imagen, 67, 35, 33, 25, int(ancho) - 12, 0 + int(alto) + 12 + 12)




pilas.iniciar()
a = Globo("Hola mundo!!!")
pilas.ejecutar()