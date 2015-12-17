# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import re
from pilasengine.interfaz import elemento

class IngresoDeTexto(elemento.Elemento):

    def __init__(self, pilas=None, texto_inicial='', x=0, y=0, ancho=300, limite_de_caracteres=20, icono=None):
        super(IngresoDeTexto, self).__init__(pilas, x=x, y=y)
        self.texto = texto_inicial
        self.cursor = ""
        self._cargar_lienzo(ancho)

        if icono:
            self.icono = self.pilas.imagenes.cargar(icono)
        else:
            self.icono = None

        self.imagen_caja = self.pilas.imagenes.cargar("interfaz/caja.png")
        self.centro = ("centro", "centro")
        self._actualizar_imagen()
        self.limite_de_caracteres = limite_de_caracteres
        self.cualquier_caracter()

        self.pilas.escena.suelta_tecla.conectar(self.cuando_pulsa_una_tecla)
        self.pilas.escena_actual().tareas.siempre(0.40, self._actualizar_cursor)
        self.fijo = True

    def _actualizar_cursor(self):
        if (self.tiene_el_foco):
            if self.cursor == "":
                self.cursor = "_"
            else:
                self.cursor = ""
        else:
            self.cursor = ""

        self._actualizar_imagen()
        return True

    def cualquier_caracter(self):
        self.caracteres_permitidos = re.compile(".*")

    def solo_numeros(self):
        self.caracteres_permitidos = re.compile("\d+")

    def solo_letras(self):
        self.caracteres_permitidos = re.compile("[a-z]+")

    def cuando_pulsa_una_tecla(self, evento):
        if self.tiene_el_foco and self.activo:
            if evento.codigo == '\x08' or evento.texto == '\x08':
                # Indica que se quiere borrar un caracter
                self.texto = self.texto[:-1]
            else:
                if len(self.texto) < self.limite_de_caracteres:
                    nuevo_texto = self.texto + evento.texto

                    if (self.caracteres_permitidos.match(evento.texto)):
                        self.texto = self.texto + evento.texto
                    else:
                        print "Rechazando el ingreso del caracter:", evento.texto
                else:
                    print "Rechazando caracter por llegar al limite."

            self._actualizar_imagen()

    def _cargar_lienzo(self, ancho):
        self.imagen = self.pilas.imagenes.cargar_superficie(ancho, 30)

    def _actualizar_imagen(self):
        ancho = self.imagen_caja.ancho()
        alto = self.imagen_caja.alto()
        self.imagen.pintar_parte_de_imagen(self.imagen_caja, 0, 0, 40, ancho, 0, 0)

        if self.icono:
            dx = 20
            self.imagen.pintar_parte_de_imagen(self.icono, 0, 0, 40, ancho, 7, 7)
        else:
            dx = 0

        for x in range(40, self.imagen.ancho() - 40):
            self.imagen.pintar_parte_de_imagen(self.imagen_caja, ancho - 40, 0, 40, alto, x, 0)

        self.imagen.texto(self.texto + self.cursor, 15 + dx, 10)