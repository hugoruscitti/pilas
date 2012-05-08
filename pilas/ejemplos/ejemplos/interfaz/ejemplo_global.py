# -*- encoding: utf-8 -*-
import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

# Boton
boton = pilas.interfaz.Boton("Hola mundo")
boton.x = -200

def cuando_hacen_click():
    boton.decir("Has pulsado el boton!")

boton.conectar(cuando_hacen_click)

# Deslizados
def cuando_cambia_posicion(valor):
    boton.x = -200 + 400 * valor

deslizador = pilas.interfaz.Deslizador(y=100)
deslizador.conectar(cuando_cambia_posicion)

# Entrada de texto
entrada1 = pilas.interfaz.IngresoDeTexto()
entrada1.texto = "Prueba 1"
entrada1.y = -50

entrada2 = pilas.interfaz.IngresoDeTexto()
entrada2.texto = "Prueba 2"
entrada2.y = -80

# Lista de selecci�n
def cuando_selecciona(opcion_seleccionada):
    pilas.avisar("Ha seleccionado la opcion: " + opcion_seleccionada)

opciones = pilas.interfaz.ListaSeleccion(['hola', 'opcion', 'tres'], cuando_selecciona)
opciones.y = -130

# Selector

selector_activar = pilas.interfaz.Selector("Activar/Desactivar interfaz", x=-200, y=200)

def cuando_el_selector_activar_cambia(estado):
    if estado:
        boton.desactivar()
        deslizador.desactivar()
        entrada1.desactivar()
        entrada2.desactivar()
        opciones.desactivar()
    else:
        boton.activar()
        deslizador.activar()
        entrada1.activar()
        entrada2.activar()
        opciones.activar()


selector_activar.definir_accion(cuando_el_selector_activar_cambia) 

selector_ocultar = pilas.interfaz.Selector("Mostrar/Ocultar interfaz", x=0, y=200)

def cuando_el_selector_ocultar_cambia(estado):
    if estado:
        boton.ocultar()
        deslizador.ocultar()
        entrada1.ocultar()
        entrada2.ocultar()
        opciones.ocultar()
    else:
        boton.mostrar()
        deslizador.mostrar()
        entrada1.mostrar()
        entrada2.mostrar()
        opciones.mostrar()


selector_ocultar.definir_accion(cuando_el_selector_ocultar_cambia) 


pilas.ejecutar()
