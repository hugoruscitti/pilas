# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
import re
from pilas.interfaz.base_interfaz import BaseInterfaz

class IngresoDeTexto(BaseInterfaz):
    """Representa una caja de texto para escribir sobre ella."""

    def __init__(self, texto_inicial="", x=0, y=0, ancho=300, limite_de_caracteres=20, icono=None):
        """Inicializa la caja de texto.

        :param texto_inicial: La cadena de texto inicial del campo de texto.
        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param ancho: Ancho de la caja para ingresar texto.
        :param limite_de_caracteres: Límite de la longitud de cadena (en cantidad de caracteres).
        :param icono: Icono que se mostrará en la cada de texto.
        """
        BaseInterfaz.__init__(self, x=x, y=y)
        self.texto = texto_inicial
        self.cursor = ""
        self._cargar_lienzo(ancho)

        if icono:
            self.icono = pilas.imagenes.cargar(icono)
        else:
            self.icono = None

        self.imagen_caja = pilas.imagenes.cargar("interfaz/caja.png")
        self.centro = ("centro", "centro")
        self._actualizar_imagen()
        self.limite_de_caracteres = limite_de_caracteres
        self.cualquier_caracter()

        self.escena.suelta_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea_siempre(0.40, self._actualizar_cursor)
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
                        print("Rechazando el ingreso del caracter:", evento.texto)
                else:
                    print("Rechazando caracter por llegar al limite.")

            self._actualizar_imagen()

    def _cargar_lienzo(self, ancho):
        self.imagen = pilas.imagenes.cargar_superficie(ancho, 30)

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
