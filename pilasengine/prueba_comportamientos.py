# coding: utf-8
import sys

sys.path.append('./')
sys.path.append('../')
sys.path.append('../..')

import pilasengine
import math

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)    # reinicia pilas automaticamente cuando
                                       # se edita y guarda este archivo.


class DarUnGiroCompleto(pilasengine.comportamientos.Comportamiento):
    pass


# Vinculamos todas las habilidades para poder utilizarlas.
pilas.comportamientos.vincular(AvanzaAIzquierda)
aceituna = pilas.actores.Aceituna()
aceituna.aprender("AvanzaAIzquierda", 1)

pilas.ejecutar()
