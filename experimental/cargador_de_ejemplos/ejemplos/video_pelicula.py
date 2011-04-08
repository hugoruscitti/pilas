import pilas

pilas.iniciar()

un = pilas.video.DePelicula('calle_buenos_aires.avi')
un.escala = [0.5]
un.rotacion = [360]

pilas.ejecutar()
