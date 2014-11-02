# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas


pilas.iniciar()


def cuando_selecciona(opcion_seleccionada):
    global seleccion
    detener_interpolacion()
    seleccion = opcion_seleccionada
    interpolacion.texto = "Interpolacion: " + seleccion

def detener_interpolacion():
    pilas.utils.detener_interpolacion(actor, 'y')
    pilas.utils.detener_interpolacion(actor, 'x')

def cuando_click(evento):
    global seleccion
    if evento.boton == 1:
        print(seleccion)
        actor.y = pilas.interpolar(evento.y,tipo=seleccion)
        actor.x = pilas.interpolar(evento.x,tipo=seleccion)

def actualizar(evento):
    velocidad.texto = "Velocidad (x,y): (%f, %f)" %(actor.vx, actor.vy)

opciones = pilas.interfaz.ListaSeleccion(['lineal',
                                          'aceleracion_gradual',
                                          'desaceleracion_gradual',
                                          'rebote_inicial',
                                          'rebote_final'], cuando_selecciona)

seleccion = 'lineal'

opciones.x = -200
opciones.y = 150

boton = pilas.interfaz.Boton("Detener Interpolacion")
boton.conectar(detener_interpolacion)

boton.x = -200

interpolacion = pilas.actores.Texto("Interpolacion: " + seleccion, x=-180, y=230)
velocidad = pilas.actores.Texto("", x=-200, y=-100)

actor = pilas.actores.Banana()
actor.y = 200

actor.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.escena_actual().click_de_mouse.conectar(cuando_click)
pilas.escena_actual().actualizar.conectar(actualizar)

pilas.ejecutar()
