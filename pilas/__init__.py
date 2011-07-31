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
import sonidos
import colores
import atajos
import escenas
import ejemplos
import interfaz


if utils.esta_en_sesion_interactiva():
    utils.cargar_autocompletado()

def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='qtgl', 
            modo='detectar', rendimiento=60, economico=True, 
            gravedad = (0, -90), pantalla_completa=False):
    global mundo

    motor = __crear_motor(usar_motor)
    mundo = Mundo(motor, ancho, alto, titulo, rendimiento, economico, gravedad, pantalla_completa)
    escenas.Normal(colores.grisclaro)


def ejecutar(ignorar_errores=False):
    "Pone en funcionamiento las actualizaciones y dibujado."
    mundo.ejecutar_bucle_principal(ignorar_errores)

def terminar():
    "Finaliza la ejecución de pilas y cierra la ventana principal."
    mundo.terminar()


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
    "Genera instancia del motor multimedia en base a un nombre."

    if usar_motor == 'qt':
        from motores import motor_qt
        motor = motor_qt.Qt()
    elif usar_motor == 'qtgl':
        from motores import motor_qt
        motor = motor_qt.QtGL()
    else:
        print "El motor multimedia seleccionado (%s) no esta disponible" %(usar_motor)
        print "Las opciones de motores que puedes probar son 'qt' y 'qtgl'."
        sys.exit(1)

    return motor

def reiniciar():
    actores.utils.eliminar_a_todos()
    mundo.reiniciar()

anterior_texto = None

def avisar(mensaje):
    "Emite un mensaje en la ventana principal."
    global anterior_texto
    izquierda, derecha, arriba, abajo = utils.obtener_bordes()

    if anterior_texto:
        anterior_texto.eliminar()

    texto = actores.Texto(mensaje)
    texto.magnitud = 17
    texto.centro = ("centro", "centro")
    texto.izquierda = izquierda + 10
    texto.color = colores.blanco
    texto.abajo = abajo + 10
    anterior_texto = texto

def abrir_cargador():
    import cargador
    cargador.ejecutar()
