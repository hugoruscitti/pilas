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

class IngresoDeTexto(Componente):
    
    def __init__(self, x=0, y=0):
        Componente.__init__(self, x=x, y=y)
        self.texto = ""
        self.cursor = "|"
        self._cargar_lienzo()
        self._cargar_imagenes(pilas)
        self._actualizar_imagen()

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea(0.25, self._actualizar_cursor)
        
    def _actualizar_cursor(self):
        if self.cursor == "":
            self.cursor = "|"
        else:
            self.cursor = ""
            
        self._actualizar_imagen()
        return True
        
    def _cargar_imagenes(self, pilas):
        self.imagen_caja = pilas.imagenes.cargar("gui/caja.png")
        
    def cuando_pulsa_una_tecla(self, evento):
        if evento.codigo == '\x08':
            # Indica que se quiere borrar un caracter
            self.texto = self.texto[:-1]
        else:
            if len(self.texto) < 23:
                self.texto = self.texto + evento.codigo
        
        self._actualizar_imagen()
        
    def _cargar_lienzo(self):
        self.lienzo = pilas.imagenes.cargar_lienzo(333, 30)
        
    def _actualizar_imagen(self):
        self.lienzo.pintar_imagen(self.imagen_caja)
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(self.texto + self.cursor, 35, 20, tamano=14, fuente='sans')
        self.lienzo.asignar(self)


s1 = Selector("Me gusta este selector !", x=-300, y=200)        
entrada = IngresoDeTexto()

   
#deslizador = pilas.actores.Deslizador()
#print deslizador.progreso
# retorna 0

# si el usuario mueve el deslizador al centro,
# progreso tendria que ser de 50, y si
# completa todo el valor tendria que ser
# de 100.

pilas.fondos.Blanco()

pilas.ejecutar()