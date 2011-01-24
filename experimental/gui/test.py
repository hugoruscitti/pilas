import pilas
pilas.iniciar()


class Componente(pilas.actores.Actor):
    def __init__(self, x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)



class Selector(Componente):
    
    def __init__(self, texto, x=0, y=0, ancho=200):
        Componente.__init__(self, x=x, y=y)
        
        self.texto = texto
        self._cargar_lienzo(ancho)
        self._cargar_imagenes(pilas)

        self.deseleccionar()
        pilas.eventos.click_de_mouse.conectar(self.detection_click_mouse)

    def _cargar_imagenes(self, pilas):
        self.imagen_selector = pilas.imagenes.cargar_imagen_cairo("gui/selector.png")
        self.imagen_selector_seleccionado = pilas.imagenes.cargar_imagen_cairo("gui/selector_seleccionado.png")

    def _cargar_lienzo(self, ancho):
        self.lienzo = pilas.imagenes.cargar_lienzo(ancho, 29)
        
    def pintar_texto(self):
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(self.texto, 35, 20, tamano=14, fuente='sans')
        
    def deseleccionar(self):
        self.seleccionado = False
        self.lienzo.deshabilitar_actualizacion_automatica()
        self.lienzo.limpiar()
        self.lienzo.pintar_imagen(self.imagen_selector)
        self.pintar_texto()
        self.lienzo.asignar(self)
        self.centro = ("centro", "centro")
        self.lienzo.habilitar_actualizacion_automatica()
        
    def seleccionar(self):
        self.seleccionado = True
        self.lienzo.deshabilitar_actualizacion_automatica()
        self.lienzo.limpiar()
        self.lienzo.pintar_imagen(self.imagen_selector_seleccionado)
        self.pintar_texto()
        self.lienzo.asignar(self)
        self.centro = ("centro", "centro")
        self.lienzo.habilitar_actualizacion_automatica()
                
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
        self.imagen_caja = pilas.imagenes.cargar_imagen_cairo("gui/caja.png")
        
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
        self.centro = ("centro", "centro")


s1 = Selector("Me gusta este selector !", x=0, y=200)        
entrada = IngresoDeTexto()


#pilas.fondos.Blanco()

pilas.ejecutar()
