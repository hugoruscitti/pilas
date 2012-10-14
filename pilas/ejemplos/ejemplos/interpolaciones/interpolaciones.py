# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas


pilas.iniciar()

def cuando_selecciona(opcion_seleccionada):
    actor.y = 200
    actor.y = pilas.interpolar(-200,2,tipo=opcion_seleccionada)

def detener_interpolacion():
    pilas.utils.deneter_interpolacion(actor, 'y')        

opciones = pilas.interfaz.ListaSeleccion(['lineal',
                                          'aceleracion_gradual',
                                          'desaceleracion_gradual',
                                          'rebote_inicial',
                                          'rebote_final'], cuando_selecciona)
opciones.x = -200
opciones.y = 150

boton = pilas.interfaz.Boton("Detener Interpolacion")
boton.conectar(detener_interpolacion)

boton.x = -200

actor = pilas.actores.Banana()
actor.y = 200


pilas.ejecutar()
