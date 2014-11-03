# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

mundo = None
bg = None

import sys
from . import utils
from .mundo import Mundo
from . import actores
from . import grupo
from . import escena
from . import fondos
from . import habilidades
from . import sonidos
from . import musica
from . import colores
from . import demos
from . import atajos
from . import interfaz
from . import interprete
from . import manual
from . import tutoriales
from . import municion
from . import dev
from pilas.escena import Normal

# Permite cerrar el programa usando CTRL+C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


__doc__ = """
Módulo pilas
============

Pilas es una biblioteca para facilitar el desarrollo
de videojuegos. Es útil para programadores
principiantes o para el desarrollo de juegos casuales.

Este módulo contiene las funciones principales
para iniciar y ejecutar la biblioteca.
"""


def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='qtgl',
            rendimiento=60, modo=None, area_fisica=None, gravedad=(0, -90), pantalla_completa=False,
            permitir_depuracion=True, audio=None, centrado=True):
    """
    Inicia la ventana principal del juego con algunos detalles de funcionamiento.

    Ejemplo de invocación:

        >>> pilas.iniciar(ancho=320, alto=240)

    .. image:: images/iniciar_320_240.png

    Parámetros:

    :ancho: el tamaño en pixels para la ventana.
    :alto: el tamaño en pixels para la ventana.
    :titulo: el titulo a mostrar en la ventana.
    :usar_motor: el motor multimedia a utilizar, puede ser 'qt', 'qtgl', 'qtsugar' o 'qtsugargl'.
    :rendimiento: cantidad de cuadros por segundo a mostrar.
    :modo: si se utiliza modo interactivo o no.
    :area_fisica: recibe una tupla con el ancho y el alto que tendra el mundo de fisica, por defecto sera el tamaño de la ventana
    :gravedad: el vector de aceleracion para la simulacion de fisica.
    :pantalla_completa: si debe usar pantalla completa o no.
    :permitir_depuracion: si se desea tener habilidatas las funciones de depuracion de las teclas F5 a F12
    :audio: selecciona el motor de sonido a utilizar, los valores permitidos son 'deshabilitado', 'pygame', 'phonon' o 'gst'.
    :centrado: Indica si se desea centrar la ventana de pilas.
    """

    global mundo

    if not esta_inicializada():
        configuracion = obtener_configuracion()

        if not usar_motor:
            usar_motor = configuracion['usar_motor']

        if not audio:
            audio = configuracion['audio']

        motor = _crear_motor(usar_motor, permitir_depuracion, audio)

        if motor:
            mundo = Mundo(motor, ancho, alto, titulo, rendimiento, area_fisica, gravedad, pantalla_completa, centrado)
            mundo.gestor_escenas.cambiar_escena(Normal())

            if _usa_interprete_lanas():
                mundo.motor.ventana.show()
    else:
        mundo.motor.modificar_ventana(ancho, alto, titulo, pantalla_completa)
        escena_actual().fisica.definir_gravedad(*gravedad)


def esta_inicializada():
    "Indica si la biblioteca pilas ha sido inicializada con pilas.iniciar()"
    global mundo
    return isinstance(mundo, Mundo)


def iniciar_con_lanzador(ancho=640, alto=480, titulo='Pilas', rendimiento=60,
                         modo='detectar', area_fisica=None, gravedad=(0, -90), imagen="asistente.png",
                         permitir_depuracion=True):
    """Identica a la función iniciar, solo que permite al usuario seleccionar
    el motor multimedia y el modo de video a utilizar.

    Esta función es útil cuando se quiere distribuir un juego y no se conoce
    exáctamente el equipo del usuario.
    """
    from . import lanzador

    usar_motor, pantalla_completa, audio = lanzador.ejecutar(imagen, titulo)
    iniciar(ancho, alto, titulo, usar_motor, rendimiento, modo, area_fisica, gravedad, pantalla_completa, permitir_depuracion, audio)


def abrir_asistente():
    """Abre una ventana que permite iniciar pilas graficamente.

    Las opciones que ofrece son "leer el manual" (si esta disponible),
    "abrir un interprete", "explorar los ejemplos" etc.

    Esta ventana se ha diseñado para mostrarse a los nuevos usuarios
    de pilas, por ejemplo cuando eligen abrir pilas desde el icono principal.
    """
    from . import asistente
    asistente.ejecutar()


def ejecutar(ignorar_errores=False):
    """Pone en funcionamiento las actualizaciones y dibujado.

    Esta función es necesaria cuando se crea un juego
    en modo ``no-interactivo``."""
    mundo.ejecutar_bucle_principal()


def terminar():
    """Finaliza la ejecución de pilas y cierra la ventana principal."""
    mundo.terminar()


def ver(objeto, imprimir=True, retornar=False):
    """Imprime en pantalla el codigo fuente asociado a un objeto."""
    return utils.ver_codigo(objeto, imprimir, retornar)


def version():
    """Retorna el número de version de pilas."""
    from . import pilasversion
    return pilasversion.VERSION


def _crear_motor(usar_motor, permitir_depuracion, audio):
    """Genera instancia del motor multimedia en base a un nombre.

    Esta es una función interna y no debe ser ejecutada
    excepto por el mismo motor pilas."""

    if usar_motor in ['qt', 'qtgl', 'qtwidget', 'qtsugar', 'qtsugargl']:
        from .motores import motor_qt

        if _usa_interprete_lanas():
            usar_motor = 'qtsugar'

        motor = motor_qt.Motor(usar_motor, permitir_depuracion, audio)
    else:
        print("El motor multimedia seleccionado (%s) no esta disponible" % (usar_motor))
        print("Las opciones de motores que puedes probar son 'qt', 'qtgl', 'qtwidget', 'qtsugar' y 'qtsugargl'.")
        motor = None

    return motor


def _usa_interprete_lanas():
    "Retorna True si se ha iniciado pilas desde lanas"
    import os
    return 'lanas' in os.environ


def reiniciar():
    """Elimina todos los actores y vuelve al estado inicial."""
    mundo.reiniciar()


def avisar(mensaje, retraso=5):
    """Emite un mensaje en la ventana principal.

    Este mensaje aparecerá en la parte inferior de la pantalla durante
    5 segundo, por ejemplo:

        >>> pilas.avisar("Use la tecla <esc> para terminar el programa")
    """
    actores.TextoInferior(mensaje, autoeliminar=True, retraso=retraso)


def abrir_cargador():
    """Abre un cargador de ejemplos con varios códigos de prueba.

    Ejemplo:

        >>> pilas.abrir_cargador()

    El cargador de ejemplos se ve de esta forma:

    .. image:: images/cargador.png
    """

    try:
        from . import ejemplos
        ejemplos.ejecutar()
    except ImportError:
        print("Lo siento, no tienes instalada la extesion de ejemplos.")
        print("Instale el paquete 'pilas-examples' para continuar.")

    return []


def abrir_interprete(parent=None, do_raise=False, con_aplicacion=False):
    """Abre un intérprete interactivo de python con una ventana.

    Esta función se ejecuta cuando un usuario escribe::

        pilas -i

    en una consola del sistema.
    """
    if con_aplicacion:
        from PyQt4 import QtGui
        app = QtGui.QApplication(sys.argv)
        app.setApplicationName("pilas-engine")

    interprete.main(parent, do_raise)
    return app


def log(*parametros):
    global mundo
    mundo.motor.log(parametros)

interpolar = utils.interpolar


def escena_actual():
    return mundo.gestor_escenas.escena_actual()


def cambiar_escena(escena):
    mundo.gestor_escenas.cambiar_escena(escena)


def almacenar_escena(escena):
    mundo.gestor_escenas.almacenar_escena(escena)


def recuperar_escena():
    mundo.gestor_escenas.recuperar_escena()


def obtener_configuracion():
    """Retorna la configuración del usuario almacenada en su directorio HOME.

    La configuración permite definir los valores por omisión cuando
    se abre la ventana de pilas. Por ejemplo, si se llama a ``pilas.iniciar()``
    sin argumentos, los valores de 'motor' o 'sistema de sonido' a utilizar
    se cargarán desde esa configuración.
    """
    opciones = {}
    opciones['usar_motor'] = 'qtgl'
    opciones['audio'] = 'pygame'
    return opciones

# Representa el viejo acceso al modulo eventos, pero convierte cada uno
# de los eventos en una referencia al evento dentro de la escena actual.
from .evento import ProxyEventos
eventos = ProxyEventos()

