# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class ColisionesFisicas(pilas.escenas.Normal):

    def __init__(self):
        pilas.escenas.Normal.__init__(self, pilas.colores.grisoscuro)
        pilas.avisar("Un ejemplo de colisiones")

        pilas.fondos.Pasto()

        m = pilas.actores.Mono()
        m.aprender(pilas.habilidades.Arrastrable)
        m.aprender(pilas.habilidades.ColisionableComoPelota)

        b = pilas.actores.Bomba()
        b.aprender(pilas.habilidades.RebotarComoPelota)

        pilas.atajos.fabricar(pilas.actores.Pelota, 20)
