# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas


class Ayuda(pilas.escenas.Escena):
    "Escena que entrega instrucciones de como jugar."

    def __init__(self):
        pilas.escenas.Escena.__init__(self) 
        pilas.actores.utils.eliminar_a_todos()
        pilas.fondos.Fondo('data/ayuda.png')
        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)

    def cuando_se_presione_escape(self, *k, **kv):
        "Regresa al menu principal"
        import escena_menu
        escena_menu.EscenaMenu()
