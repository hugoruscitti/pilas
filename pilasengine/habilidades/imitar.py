# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades
from pilasengine import fisica


class Imitar(habilidades.Habilidad):
    "Logra que el actor imite las propiedades de otro."

    def iniciar(self, receptor, objeto_a_imitar, con_escala=True,
                con_rotacion=True):
        """Inicializa la habilidad.

        :param receptor: Referencia al actor.
        :param objeto_a_imitar: Cualquier objeto con atributos rotacion,
                                x e y (por ejemplo otro actor).
        :param con_rotacion: Si debe imitar o no la rotación.
        """
        super(Imitar, self).iniciar(receptor)
        self.objeto_a_imitar = objeto_a_imitar

        # Establecemos el mismo id para el actor y el objeto fisico
        # al que imita. Así luego en las colisiones fisicas sabremos a que
        # actor corresponde esa colisión.
        receptor.id = objeto_a_imitar.id

        # Y nos guardamos una referencia al objeto físico al que imita.
        # Posterormente en las colisiones fisicas comprobaremos si el
        # objeto tiene el atributo "figura" para saber si estamos delante
        # de una figura fisica o no.
        if hasattr(objeto_a_imitar, '_cuerpo'):
            receptor.figura = objeto_a_imitar
            receptor.figura_de_colision = objeto_a_imitar

        self.con_escala = con_escala
        self.con_rotacion = con_rotacion

        self.imitar()

    def actualizar(self):
        self.imitar()

    def imitar(self):
        self.receptor.x = self.objeto_a_imitar.x
        self.receptor.y = self.objeto_a_imitar.y

        if self.con_escala:
            self.objeto_a_imitar.escala = self.receptor.escala

        if self.con_rotacion:
            self.receptor.rotacion = self.objeto_a_imitar.rotacion

    def eliminar(self):
        super(Imitar, self).eliminar()
        if isinstance(self.objeto_a_imitar, fisica.figura.Figura):
            self.objeto_a_imitar.eliminar()
            self.receptor.figura = None