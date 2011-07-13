import pilas

pilas.iniciar()

def selecciona_iniciar():
    pilas.avisar("Ha seleccionado Iniciar")

def selecciona_terminar():
    pilas.avisar("Ha seleccionado Terminar")


opciones = [
            ('Iniciar', selecciona_iniciar),
            ('Terminar', selecciona_terminar)]


pilas.avisar("Use el teclado para cambiar o seleccionar opciones.")
menu = pilas.actores.Menu(opciones)


pilas.ejecutar()
