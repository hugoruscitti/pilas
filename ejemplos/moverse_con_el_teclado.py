import pilas

mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.avisar("Use los direccionales del teclado para mover al mono.")
pilas.ejecutar()
