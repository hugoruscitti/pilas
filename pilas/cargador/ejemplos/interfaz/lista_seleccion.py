import pilas

pilas.iniciar()
pilas.fondos.Pasto()

def cuando_selecciona(opcion_seleccionada):
    pilas.avisar("Ha seleccionado la opcion: " + opcion_seleccionada)

opciones = pilas.interfaz.ListaSeleccion(['hola', 'opcion', 'tres'], cuando_selecciona)
pilas.avisar("Selecciona alguna de las opciones...")

pilas.ejecutar()
