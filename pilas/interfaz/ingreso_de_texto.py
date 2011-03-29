# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class IngresoDeTexto(pilas.actores.Actor):
    
    def __init__(self, x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        self.texto = ""
        self.cursor = "|"
        self._cargar_lienzo()
        self._cargar_imagenes(pilas)
        self._actualizar_imagen()

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea_siempre(0.25, self._actualizar_cursor)
        
    def _actualizar_cursor(self):
        if self.cursor == "":
            self.cursor = "|"
        else:
            self.cursor = ""
            
        self._actualizar_imagen()
        return True
        
    def _cargar_imagenes(self, pilas):
        self.imagen_caja = pilas.imagenes.cargar_imagen_cairo("interfaz/caja.png")
        
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
