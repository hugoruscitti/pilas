import pilas
pilas.iniciar()


class Componente(pilas.actores.Actor):
    def __init__(self, x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)



class Selector(Componente):
    
    def __init__(self, texto, x=0, y=0, ancho=200):
        Componente.__init__(self, x=x, y=y)
        
        self._cargar_lienzo(texto, ancho)
        self._cargar_imagenes(pilas)

        self.deseleccionar()
        pilas.eventos.click_de_mouse.conectar(self.detection_click_mouse)

    def _cargar_imagenes(self, pilas):
        self.imagen_selector = pilas.imagenes.cargar("gui/selector.png")
        self.imagen_selector_rojo = pilas.imagenes.cargar("gui/selector_rojo.png")

    def _cargar_lienzo(self, texto, ancho):
        self.lienzo = pilas.imagenes.cargar_lienzo(ancho, 29)
        self.lienzo.pintar(pilas.colores.blanco)
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(texto, 35, 20, tamano=14, fuente='sans')
        
    def deseleccionar(self):
        self.seleccionado = False
        self.lienzo.pintar_imagen(self.imagen_selector)
        self.lienzo.asignar(self)
        self.centro = ("izquierda", "centro")
        
    def seleccionar(self):
        self.seleccionado = True
        self.lienzo.pintar_imagen(self.imagen_selector_rojo)
        self.lienzo.asignar(self)
        self.centro = ("izquierda", "centro")
                
    def detection_click_mouse(self, click):
        if self.colisiona_con_un_punto(click.x, click.y):
            self.alternar_seleccion()
                
    def alternar_seleccion(self):
        if self.seleccionado:
            self.deseleccionar()
        else:
            self.seleccionar()
            
            
s1 = Selector("Me gusta este selector !", x=-300, y=200)        


   
#deslizador = pilas.actores.Deslizador()
#print deslizador.progreso
# retorna 0

# si el usuario mueve el deslizador al centro,
# progreso tendria que ser de 50, y si
# completa todo el valor tendria que ser
# de 100.

pilas.fondos.Blanco()

pilas.ejecutar()