# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

pilas.iniciar(titulo = "Memorice")




# ejecuta escena actual.
from . import escena_menu
pilas.cambiar_escena(escena_menu.EscenaMenu())



pilas.ejecutar()
