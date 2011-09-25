# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.actores import Actor
import pilas

class EntradaDeTexto(Actor):
    """Representa una caja de texto que puede servir para ingresar texto.
    
    Este actor, en la mayoria de los casos, se utiliza para solicitarle
    el nombre a un usuario. Por ejemplo, cuando completa un record
    de puntaje."""

    def __init__(self, x=0, y=0, color=pilas.colores.negro, limite=10, tamano=32, fuente='Arial', cursor_intermitente=True):
        self.cursor = "|"
        self.texto = ""
        self.limite = limite
        imagen = pilas.imagenes.cargar_superficie(640, 480)
        Actor.__init__(self, imagen)
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        self._actualizar_imagen()
        
        if cursor_intermitente:
            pilas.mundo.agregar_tarea_siempre(0.25, self._actualizar_cursor)

    def _actualizar_cursor(self):
        if self.cursor == "":
            self.cursor = "|"
        else:
            self.cursor = ""

        self._actualizar_imagen()
        return True


    def cuando_pulsa_una_tecla(self, evento):
        if evento.codigo == '\x08':
            # Indica que se quiere borrar un caracter
            self.texto = self.texto[:-1]
        else:
            if len(self.texto) < self.limite:
                self.texto = self.texto + evento.texto
        
        self._actualizar_imagen()
        
    def _actualizar_imagen(self):
        self.imagen.pintar(pilas.colores.blanco)
        self.imagen.texto(self.texto + self.cursor, 100, 100)
