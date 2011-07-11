# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class IngresoDeTexto(pilas.actores.Actor):
    
    def __init__(self, texto_inicial="", x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        self.texto = texto_inicial
        self.cursor = ""
        self._cargar_lienzo()
        self.imagen_caja = pilas.imagenes.cargar("interfaz/caja.png")
        self.centro = ("centro", "centro")
        self._actualizar_imagen()


        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea_siempre(0.40, self._actualizar_cursor)
        
    def _actualizar_cursor(self):
        if self.cursor == "":
            self.cursor = "_"
        else:
            self.cursor = ""
            
        self._actualizar_imagen()
        return True
        
        
    def cuando_pulsa_una_tecla(self, evento):
        if evento.codigo == '\x08' or evento.texto == '\x08':
            # Indica que se quiere borrar un caracter
            self.texto = self.texto[:-1]
        else:
            if len(self.texto) < 23:
                self.texto = self.texto + evento.texto
        
        self._actualizar_imagen()
        
    def _cargar_lienzo(self):
        self.imagen = pilas.imagenes.cargar_superficie(400, 200)
        
    def _actualizar_imagen(self):
        self.imagen.pintar_imagen(self.imagen_caja)
        self.imagen.texto(self.texto + self.cursor, 35, 20)
