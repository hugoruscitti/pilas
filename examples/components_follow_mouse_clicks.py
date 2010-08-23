import pilas

mono = pilas.actores.Mono()
mono.aprender(pilas.comportamientos.SeguirClicks)
mono.aprender(pilas.comportamientos.AumentarConRueda)

pilas.bucle()
