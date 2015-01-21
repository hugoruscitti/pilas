import pilasengine

pilas = pilasengine.iniciar()
protagonista = pilas.actores.Aceituna()
protagonista.aprender(pilas.habilidades.SeguirAlMouse)
pilas.ocultar_puntero_del_mouse()

pilas.ejecutar()
