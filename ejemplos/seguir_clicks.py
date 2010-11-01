# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.SeguirClicks)
mono.aprender(pilas.habilidades.AumentarConRueda)

pilas.avisar("El mono sigue los clicks, y cambia de tamaño si mueves la\nrueda del mouse.")
pilas.ejecutar()
