import pilas
pilas.iniciar()

selector = pilas.interfaz.Selector("Usar fondo", x=0, y=0)
fondo = None

def cuando_el_selector_cambia(estado):
    global fondo

    if estado:
        fondo = pilas.fondos.Pasto()
    else:
        fondo.eliminar()


selector.definir_accion(cuando_el_selector_cambia) 

pilas.ejecutar()
