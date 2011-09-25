import pilas
pilas.iniciar()


def cuando_selecciona(opcion):
    print "Ha seleccionado la opcion:", opcion


consulta = pilas.interfaz.ListaSeleccion(['Uno', 'Dos', 'Tres'], cuando_selecciona)

pilas.ejecutar()
    
