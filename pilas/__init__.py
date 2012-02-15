# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

mundo = None
bg = None

import console
import sys
import utils
from mundo import Mundo
import actores
import fondos
import habilidades
import eventos
import sonidos
#import musica
import colores
import atajos
import escenas
import interfaz

try:
    import aplicacion
    import ejemplos
except ImportError:
    print "ERROR: no está disponible PyQt4"


__doc__ = """
Módulo pilas
============

Pilas es una biblioteca para facilitar el desarrollo
de videojuegos. Es útil para programadores
principiantes o para el desarrollo de juegos casuales.

Este módulo contiene las funciones principales
para iniciar y ejecutar la biblioteca.
"""

if utils.esta_en_sesion_interactiva():
    utils.cargar_autocompletado()

def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='qt', 
            rendimiento=60, modo='detectar', gravedad=(0, -90), pantalla_completa=False):
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
    :gravedad: el vector de aceleracion para la simulacion de fisica.
    :pantalla_completa: si debe usar pantalla completa o no.

    """
    
    global mundo

    motor = _crear_motor(usar_motor)

    if motor:
        mundo = Mundo(motor, ancho, alto, titulo, rendimiento, gravedad, pantalla_completa)
        escenas.Normal(colores.grisclaro)


def ejecutar(ignorar_errores=False):
    """Pone en funcionamiento las actualizaciones y dibujado.
    
    Esta función es necesaria cuando se crea un juego
    en modo ``no-interactivo``."""
    mundo.ejecutar_bucle_principal(ignorar_errores)

def terminar():
    """Finaliza la ejecución de pilas y cierra la ventana principal."""
    mundo.terminar()

def ver(objeto, imprimir=True, retornar=False):
    """Imprime en pantalla el codigo fuente asociado a un objeto."""
    return utils.ver_codigo(objeto, imprimir, retornar)

def version():
    """Retorna el número de version de pilas."""
    import pilasversion
    return pilasversion.VERSION

def _crear_motor(usar_motor):
    """Genera instancia del motor multimedia en base a un nombre.
    
    Esta es una función interna y no debe ser ejecutada
    excepto por el mismo motor pilas."""

    if usar_motor in ['qt', 'qtgl', 'qtsugar', 'qtsugargl']:
        from motores import motor_qt
        motor = motor_qt.Motor(usar_motor)
    else:
        print "El motor multimedia seleccionado (%s) no esta disponible" %(usar_motor)
        print "Las opciones de motores que puedes probar son 'qt', 'qtgl', 'qtsugar' y 'qtsugargl'."
        motor = None

    return motor

def reiniciar():
    """Elimina todos los actores y vuelve al estado inicial."""
    actores.utils.eliminar_a_todos()
    mundo.reiniciar()

anterior_texto = None

def avisar(mensaje):
    """Emite un mensaje en la ventana principal.

    Este mensaje aparecerá en la parte inferior de la pantalla, por
    ejemplo:

        >>> pilas.avisar("Use la tecla <esc> para terminar el programa")
    """
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
    """Abre un cargador de ejemplos con varios códigos de prueba.

    Ejemplo:

        >>> pilas.abrir_cargador()

    El cargador de ejemplos se ve de esta forma:

    .. image:: images/cargador.png
    """

    try:
        import ejemplos
        ejemplos.ejecutar()
    except ImportError:
        print "Lo siento, no tienes instalada la extesion de ejemplos."
        print "Instale el paquete 'pilas-examples' para continuar."

    return []

def abrir_interprete():
    """Abre un intérprete interactivo de python con una ventana.
    
    Esta función se ejecuta cuando un usuario escribe::

        pilas -i

    en una consola del sistema.
    """

    import aplicacion
    aplicacion.main()
