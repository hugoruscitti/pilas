# coding: utf-8
import pilasengine
import math

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

torrenta = pilas.actores.Torreta()

pilas.ejecutar()