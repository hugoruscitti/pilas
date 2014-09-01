# -*- encoding: utf-8 -*-
import pilasengine

import escena_menu

pilas = pilasengine.iniciar(titulo="Tres en raya")
pilas.escenas.definir_escena(escena_menu.EscenaMenu(pilas))
pilas.ejecutar()