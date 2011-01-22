import pilas

class Globo(pilas.actores.Actor):
    
    def __init__(self, texto, x=0, y=0):
        pilas.actores.Actor.__init__(self)
        self.lienzo = pilas.lienzo.Lienzo()
        imagen = pilas.imagenes.cargar_imagen_cairo("globo.png")

        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)
        
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
            self.lienzo.pintar_parte_de_imagen(imagen, 12, 35, 12, 12, 12 + x,  0 + int(alto) + 12 + 12)
        
        self.lienzo.pintar_parte_de_imagen(imagen, 100, 35, 12, 12, 12 + int(ancho) + 12, 0 + int(alto) + 12 + 12)

        # Pico de la parte de abajo
        self.lienzo.pintar_parte_de_imagen(imagen, 67, 35, 33, 25, int(ancho) - 12, 0 + int(alto) + 12 + 12)
        



        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(texto, 12, 25, tamano=14)
        self.lienzo.asignar(self)
        




pilas.iniciar()
a = Globo("Hola mundo, este.")
pilas.ejecutar()