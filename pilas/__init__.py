# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

mundo = None
bg = None

import utils
from mundo import Mundo
import actores
import fondos
import habilidades
import eventos


if utils.esta_en_sesion_interactiva():
    utils.cargar_autocompletado()


def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='qt', 
            modo='detectar', rendimiento=60, economico=True, gravedad = (0, -90)):
    global mundo

    motor = __crear_motor(usar_motor)
    mundo = Mundo(motor, ancho, alto, titulo, rendimiento, economico, gravedad)

    #pilas.colisiones = Colisiones()

    '''
    if modo == 'detectar':
        if utils.esta_en_sesion_interactiva():
            iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]", rendimiento, economico, gravedad)
        else:
            mundo = pilas.mundo.Mundo(ancho, alto, titulo, rendimiento, economico, gravedad)
            escenas.Normal()
    elif modo == 'interactivo':
        iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]", rendimiento, economico, gravedad)
    else:
        raise Exception("Lo siento, el modo indicado es invalido, solo se admite 'interactivo' y 'detectar'")
    '''

'''
def iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo, fps, economico, gravedad):
    "Ejecuta el bucle de pilas en segundo plano."
    import threading
    global gb

    bg = threading.Thread(target=__iniciar_y_ejecutar, args=(ancho, alto, titulo, fps, economico, gravedad))
    bg.start()

def reiniciar():
    actores.utils.eliminar_a_todos()

def __iniciar_y_ejecutar(ancho, alto, titulo, fps, economico, gravedad, ignorar_errores=False):
    global mundo

    mundo = Mundo(ancho, alto, titulo, fps, economico, gravedad)
    escenas.Normal()
    ejecutar(ignorar_errores)
'''

def terminar():
    "Finaliza la ejecución de pilas y cierra la ventana principal."
    global mundo
    mundo.terminar()

def ejecutar(ignorar_errores=False):
    mundo.ejecutar_bucle_principal(ignorar_errores)


'''
anterior_texto = None

def avisar(mensaje):
    "Emite un mensaje en la ventana principal."
    global anterior_texto

    if anterior_texto:
        anterior_texto.eliminar()

    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.centro = ("centro", "centro")
    texto.izquierda = -310
    texto.abajo = -230
    anterior_texto = texto



def ejecutar_cada(segundos, funcion):
    """Ejecuta una funcion con la frecuencia que indica el argumento segundos.
    
    La funcion ejecutada tiene que retornar True para volver a
    ejecutarse, si retorna False se elimina el temporizador y la funcion
    no se vuelve a ejecutar.
    """
    pilas.mundo.agregar_tarea_siempre(segundos, funcion)
'''

def ver(objeto):
    "Imprime en pantalla el codigo fuente asociado a un objeto o elemento de pilas."
    import inspect

    try:
        codigo = inspect.getsource(objeto.__class__)
    except TypeError:
        codigo = inspect.getsource(objeto)

    print codigo

def version():
    "Retorna el numero de version de pilas."
    import pilasversion

    return pilasversion.VERSION

def __crear_motor(usar_motor):
    "Genera instancia del motor multimedia en base a una cadena seleccion."

    if usar_motor == 'qt':
        from motores import motor_qt
        motor = motor_qt.Qt()
    elif usar_motor == 'pygame':
        from motores import motor_pygame
        motor = motor_pygame.Pygame()
    elif usar_motor in ['sfml', 'pysfml']:
        from motores import motor_sfml
        motor = motor_sfml.pySFML()
    else:
        print "El motor multimedia seleccionado (%s) no esta disponible" %(usar_motor)
        print "Las opciones de motores que puedes probar son 'qt', 'pygame' y 'sfml'."
        sys.exit(1)

    return motor
