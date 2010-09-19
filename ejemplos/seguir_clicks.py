import pilas

mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.SeguirClicks)
mono.aprender(pilas.habilidades.AumentarConRueda)

pilas.avisar("El mono sigue los clicks, y escala con la rueda del mouse.")
pilas.ejecutar()
