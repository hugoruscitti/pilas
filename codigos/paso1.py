import pilas

pilas.iniciar()
protagonista = pilas.actores.Aceituna()
protagonista.aprender(pilas.habilidades.SeguirAlMouse)
pilas.mundo.motor.ocultar_puntero_del_mouse()

pilas.ejecutar()

