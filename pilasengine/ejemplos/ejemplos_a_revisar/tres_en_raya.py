# -*- encoding: utf-8 -*-
import os

import pilasengine
from tres_en_raya import escena_menu


os.chdir(os.path.join(os.getcwd(), 'tres_en_raya'))
pilas = pilasengine.iniciar(titulo="Tres en raya")
pilas.escenas.definir_escena(escena_menu.EscenaMenu(pilas))
pilas.ejecutar()