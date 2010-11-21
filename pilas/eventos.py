# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import dispatch

mueve_mouse = dispatch.Signal(providing_args=['x', 'y', 'dx', 'dy'])
click_de_mouse = dispatch.Signal(providing_args=['button', 'x', 'y'])
termina_click = dispatch.Signal(providing_args=['button', 'x', 'y'])
mueve_rueda = dispatch.Signal(providing_args=['delta'])
pulsa_tecla = dispatch.Signal(providing_args=['code'])
pulsa_tecla_escape = dispatch.Signal(providing_args=[])
actualizar = dispatch.Signal(providing_args=[])
