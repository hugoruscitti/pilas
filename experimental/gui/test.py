import pilas
pilas.iniciar()


class Componente(pilas.actores.Actor):
    def __init__(self, x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)





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


s1 = pilas.interfaz.Selector("Me gusta este selector !", x=0, y=200)        
entrada = IngresoDeTexto()


#pilas.fondos.Blanco()

pilas.ejecutar()
