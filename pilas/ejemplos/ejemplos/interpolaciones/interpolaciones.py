# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas


pilas.iniciar()

def cuando_selecciona(opcion_seleccionada):
    actor.y = 200
    actor.y = pilas.interpolar(-200,2,tipo=opcion_seleccionada)

opciones = pilas.interfaz.ListaSeleccion(['lineal',
                                          'aceleracion_gradual',
                                          'desaceleracion_gradual',
                                          'rebote_inicial',
                                          'rebote_final'], cuando_selecciona)
opciones.x = -200
opciones.y = 150

actor = pilas.actores.Banana()
actor.y = 200


pilas.ejecutar()
