# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine

pilas = pilasengine.iniciar()

aceituna = pilas.actores.Aceituna()

aceituna.aprender(pilas.habilidades.SiempreEnElCentro)
aceituna.x = [100], 2
aceituna.y = [100], 2

pilas.ejecutar()