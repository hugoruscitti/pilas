#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo pilas.escena
===================

"""
import pilas

from .gestor import Gestor
from .escena_base import Base
from .escena_normal import Normal
from .escena_pausa import Pausa
from .escena_normal import Aviso
from .escena_logos import Logos

def pausar():
    """Hace que la ejecución del juego se PAUSE y pulsando la tecla ESC 
    vuelves al juego."""
    class Escena_Pausa(Pausa):

        def __init__(self):
            Pausa.__init__(self)

        def iniciar(self):
            self.pausa = pilas.actores.Pausa()
            self.pulsa_tecla_escape.conectar(self.recuperar_escena_anterior)

        def recuperar_escena_anterior(self, evento):
            pilas.recuperar_escena()

    pilas.almacenar_escena(Escena_Pausa())
