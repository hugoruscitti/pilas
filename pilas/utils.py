# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from __future__ import print_function
import os
from . import interpolaciones
import sys
import subprocess
import math
import uuid
import pilas
import mimetypes


PATH = os.path.dirname(os.path.abspath(__file__))
INTERPRETE_PATH = os.path.dirname(sys.argv[0])


def es_interpolacion(an_object):
    """Indica si un objeto se comportará como una interpolación.

    :param an_object: El objeto a consultar.
    """
    return isinstance(an_object, interpolaciones.Interpolacion)


def obtener_ruta_al_recurso(ruta):
    """Busca la ruta a un archivo de recursos.

    Los archivos de recursos (como las imagenes) se buscan en varios
    directorios (ver docstring de image.load), así que esta
    función intentará dar con el archivo en cuestión.

    :param ruta: Ruta al archivo (recurso) a inspeccionar.
    """

    dirs = ['./', INTERPRETE_PATH, INTERPRETE_PATH + '/data', 'data', PATH, PATH + '/data']

    for x in dirs:
        full_path = os.path.join(x, ruta)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." % (ruta))


def esta_en_sesion_interactiva():
    """Indica si pilas se ha ejecutado desde una consola interactiva de python."""
    import sys
    try:
        cursor = sys.ps1
        return True
    except AttributeError:
        try:
            in_ipython = sys.ipcompleter
            return True
        except AttributeError:
            if sys.stdin.__class__.__module__.startswith("idle"):
                return True

    return False


def distancia(a, b):
    """Retorna la distancia entre dos numeros.

        >>> distancia(30, 20)
        10

    :param a: Un valor numérico.
    :param b: Un valor numérico.
    """
    return abs(b - a)


def distancia_entre_dos_puntos(coords1, coords2):
    """Retorna la distancia entre dos puntos en dos dimensiones.

    :param coords1: Tupla de coordenadas (x, y) del primer punto.
    :param coords2: Tupla de coordenadas (x, y) del segundo punto.
    """
    (x1, y1) = coords1
    (x2, y2) = coords2
    return math.sqrt(distancia(x1, x2) ** 2 + distancia(y1, y2) ** 2)


def distancia_entre_dos_actores(a, b):
    """Retorna la distancia en pixels entre dos actores.

    :param a: El primer actor.
    :param b: El segundo actor.
    """
    
    dis = distancia_entre_dos_puntos((a.x, a.y), (b.x, b.y)) - a.radio_de_colision - b.radio_de_colision 
    
    if (dis < 0):
        return 0
    else:
        return dis
    


def actor_mas_cercano_al_actor(actor):
    """Retorna el actor de la escena que esté mas cercano a otro indicado por parámetro.

    :param actor: El actor tomado como referencia.
    """
    actor_mas_cercano = None
    distancia = 999999
    for actor_cercano in pilas.escena_actual().actores:
        if id(actor_cercano) != id(actor):
            if distancia_entre_dos_actores(actor, actor_cercano) < distancia:
                actor_mas_cercano = actor_cercano

    return actor_mas_cercano


def colisionan(a, b):
    """Retorna True si dos actores estan en contacto.

    :param a: Un actor.
    :param b: El segundo actor a verificar.
    """
    return distancia_entre_dos_actores(a, b) < a.radio_de_colision + b.radio_de_colision


def interpolable(f):
    """Decorador que se aplica a un metodo para que permita animaciones de interpolaciones.

    Ejemplo::

        @interpolable
        def set_x(self, valor_x):
            [...]

    :param f: Método sobre el que va a trabajar el interpolador.
    """

    def inner(*args, **kwargs):
        value = args[1]

        # Si le indican dos argumentos, el primer sera
        # el valor de la interpolacion y el segundo la
        # velocidad.
        if isinstance(value, tuple) and len(value) == 2:
            duracion = value[1]
            value = value[0]
        else:
            duracion = 1

        if isinstance(value, list):
            value = interpolar(value, duracion=duracion, tipo='lineal')
        elif isinstance(value, xrange):
            value = interpolar(list(value), duracion=duracion, tipo='lineal')

        if es_interpolacion(value):
            value.apply(args[0], function=f.__name__)
        else:
            f(args[0], value, **kwargs)

    return inner


def hacer_coordenada_mundo(x, y):
    """Convierte una coordenada de pantalla a una coordenada dentro del motor de física.

    :param x: Coordenada horizontal.
    :param y: Coordenada vertical.
    """
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)


def hacer_coordenada_pantalla_absoluta(x, y):
    # TODO: Duplicado del codigo anterior?
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)


def listar_actores_en_consola():
    """Imprime una lista de todos los actores en la escena sobre la consola."""
    todos = pilas.escena_actual().actores

    print("Hay %d actores en la escena:" % (len(todos)))
    print("")

    for s in todos:
        print("\t", s)

    print("")


def obtener_angulo_entre(punto_a, punto_b):
    """Retorna el ángulo entro dos puntos de la pantalla.

    :param punto_a: Una tupla con la coordenada del primer punto.
    :param punto_b: Una tupla con la coordenada del segundo punto.
    """
    (x, y) = punto_a
    (x1, y1) = punto_b
    return math.degrees(math.atan2(y1 - y, x1 - x))


def convertir_de_posicion_relativa_a_fisica(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)


def convertir_de_posicion_fisica_relativa(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x - dx, dy - y)


def calcular_tiempo_en_recorrer(distancia_en_pixeles, velocidad):
    """Calcula el tiempo que se tardará en recorrer una distancia en
    pixeles con una velocidad constante.

    :param distancia_en_pixeles: La longitud a recorrer medida en pixels.
    :param velocidad: La velocida medida en pixels.
    """
    if (pilas.mundo.motor.canvas.fps.cuadros_por_segundo_numerico > 0):
        return (distancia_en_pixeles / (pilas.mundo.motor.canvas.fps.cuadros_por_segundo_numerico * velocidad))
    else:
        return 0


def interpolar(valor_o_valores, duracion=1, demora=0, tipo='lineal'):
    """Retorna un objeto que representa cambios de atributos progresivos.

    El resultado de esta función se puede aplicar a varios atributos
    de los actores, por ejemplo:

        >>> bomba = pilas.actores.Bomba()
        >>> bomba.escala = pilas.interpolar(3)

    Esta función también admite otros parámetros cómo:

    :param duracion: es la cantidad de segundos que demorará toda la interpolación.
    :param demora: cuantos segundos se deben esperar antes de iniciar.
    :param tipo: es el algoritmo de la interpolación, puede ser 'lineal'.
    """

    from . import interpolaciones

    algoritmos = {
        'lineal': interpolaciones.Lineal,
        'aceleracion_gradual': interpolaciones.AceleracionGradual,
        'desaceleracion_gradual': interpolaciones.DesaceleracionGradual,
        'rebote_inicial': interpolaciones.ReboteInicial,
        'rebote_final': interpolaciones.ReboteFinal,
        'elastico_inicial': interpolaciones.ElasticoInicial,
        'elastico_final': interpolaciones.ElasticoFinal
    }

    if tipo in algoritmos:
        clase = algoritmos[tipo]
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" % (tipo))

    # Permite que los valores de interpolacion sean un numero o una lista.
    if not isinstance(valor_o_valores, list):
        valor_o_valores = [valor_o_valores]

    return clase(valor_o_valores, duracion, demora)


def detener_interpolacion(objeto, propiedad):
    """Deteiene una interpolación iniciada en un campo de un objeto.

       >>> pilas.utils.detener_interpolacion(actor, 'y')

    :param objeto: Actor del que se desea detener al interpolacion.
    :para propiedad: Cadena de texto que indica la propiedad del objeto cuya interpolación se desea terminar.
    """
    setter = 'set_' + propiedad
    try:
        getattr(objeto, setter)
        pilas.escena_actual().tweener.removeTweeningFromObjectField(objeto, setter)
    except:
        print("El obejto %s no tiene esa propiedad %s" % (objeto.__class__.__name__, setter))


def obtener_area():
    """Retorna el area que ocupa la ventana"""
    return pilas.mundo.obtener_area()


def obtener_bordes():
    """Retorna los bordes de la pantalla en forma de tupla."""
    ancho, alto = pilas.mundo.obtener_area()
    return -ancho/2, ancho/2, alto/2, -alto/2


def obtener_area_de_texto(texto):
    """Informa el ancho y alto que necesitara un texto para imprimirse.

    :param texto: La cadena de texto que se quiere imprimir.
    """
    return pilas.mundo.motor.obtener_area_de_texto(texto)


def realizar_pruebas():
    """Imprime pruebas en pantalla para detectar si pilas tiene todas las dependencias instaladas."""
    print("Realizando pruebas de dependencias:")
    print("")

    print("Box 2D:", end=' ')
    ver = pilas.fisica.obtener_version_en_tupla()
    if ver[0] == 2 and ver[1] >= 1:
        print("OK, versión", pilas.fisica.obtener_version())
    else:
        print("Error -> la versión está obsoleta, instale una versión de la serie 2.1")

    print("pyqt:", end=' ')

    try:
        from PyQt4 import Qt
        print("OK, versión", Qt.PYQT_VERSION_STR)
    except ImportError:
        print("Error -> no se encuentra pyqt.")

    print("pyqt con aceleracion:", end=' ')

    try:
        from PyQt4 import QtOpenGL
        from PyQt4.QtOpenGL import QGLWidget
        print("OK")
    except ImportError:
        print("Error -> no se encuentra pyqt4gl.")

    print("PIL para soporte de jpeg (opcional):", end=' ')

    try:
        from PIL import Image
        print("OK")
    except ImportError:
        print("Cuidado -> no se encuentra PIL.")


def ver_codigo(objeto, imprimir, retornar):
    """Imprime en pantalla el codigo fuente asociado a un objeto.

    :param objeto: El objeto que se quiere inspeccionar.
    :param imprimir: Un valor True o False indicando si se quiere imprimir directamente sobre la pantalla.
    :param retornar: Un valor True o False indicando si se quiere obtener el código como un string.
    """
    import inspect

    try:
        codigo = inspect.getsource(objeto.__class__)
    except TypeError:
        try:
            codigo = inspect.getsource(objeto)
        except TypeError:
            codigo = "<< imposible inspeccionar código para mostrar >>"

    if imprimir:
        print(codigo)

    if retornar:
        return codigo


def obtener_uuid():
    """Genera un identificador único."""
    return str(uuid.uuid4())


def abrir_archivo_con_aplicacion_predeterminada(ruta_al_archivo):
    """Intenta abrir un archivo con la herramienta recomenda por el sistema operativo.

    :param ruta_al_archivo: La ruta al archivo que se quiere abrir.
    """
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', ruta_al_archivo))
    elif os.name == 'nt':
        os.startfile(ruta_al_archivo)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', ruta_al_archivo))


def centrar_ventana(widget):
    """Coloca la ventana o widget directamente en el centro del escritorio.

    :param widget: Widget que representa la ventana.
    """
    from PyQt4 import QtGui
    desktop = QtGui.QApplication.desktop()
    widget.move(desktop.screen().rect().center() - widget.rect().center())


def descargar_archivo_desde_internet(parent, url, archivo_destino):
    """Inicia la descarga de una archivo desde Internet.

    :param parent: El widget que será padre de la ventana.
    :param url: La URL desde donde se descargará el archivo.
    :param archivo_destino: La ruta en donde se guardará el archivo.
    """
    from . import descargar
    ventana = descargar.Descargar(parent, url, archivo_destino)
    ventana.show()


def imprimir_todos_los_eventos():
    """Muestra en consola los eventos activos y a quienes invocan"""
    import pilas

    for x in dir(pilas.escena_actual()):
        attributo = getattr(pilas.escena_actual(), x)

        if isinstance(attributo, pilas.evento.Evento):
            print("Evento:", attributo.nombre)
            attributo.imprimir_funciones_conectadas()
            print("")


def habilitar_depuracion():
    """Permite habilitar un breakpoint para depuracion una vez inicializado pilas."""
    from PyQt4.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()


def mostrar_mensaje_de_error_y_salir(motivo):
    """Muestra un mensaje de error y termina con la ejecución de pilas.

    :param motivo: Un mensaje que explica el problema o la razón del cierre de pilas.
    """
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv[:1])
    app.setApplicationName("pilas-engine error")
    main_window = QtGui.QMainWindow()
    main_window.show()
    main_window.raise_()
    QtGui.QMessageBox.critical(main_window, "Error", motivo)
    app.exit()
    sys.exit(1)


def obtener_archivo_a_ejecutar_desde_argv():
    """Obtiene la ruta del archivo a ejecutar desde la linea de argumentos del programa."""
    import sys

    argv = sys.argv[:]

    if '-i' in argv:
        argv.remove('-i')

    return " ".join(argv[1:])


def procesar_argumentos_desde_command_line():
    from optparse import OptionParser


    analizador = OptionParser()

    analizador.add_option("-t", "--test", dest="test",
                          action="store_true", default=False,
                          help="Invoca varias pruebas verificar el funcionamiento de pilas")

    analizador.add_option("-v", "--version", dest="version",
                          action="store_true", default=False,
                          help="Consulta la version instalada")

    analizador.add_option("-i", "--interprete", dest="interprete",
                          action="store_true", default=False,
                          help="Abre el interprete interactivo")

    (opciones, argumentos) = analizador.parse_args()
    return (opciones, argumentos)


def iniciar_asistente_desde_argumentos():
    if sys.platform == 'darwin':
        import pilas
        pilas.abrir_asistente()
    else:
        (opciones, argumentos) = procesar_argumentos_desde_command_line()

        if argumentos:
            archivo_a_ejecutar = obtener_archivo_a_ejecutar_desde_argv()

            if not os.path.exists(archivo_a_ejecutar):
                mostrar_mensaje_de_error_y_salir("El archivo '%s' no existe o no se puede leer." % (archivo_a_ejecutar))

            if not 'text/x-python' in mimetypes.guess_type(archivo_a_ejecutar):
                mostrar_mensaje_de_error_y_salir("El archivo '%s' no parece un script python. Intenta con un archivo .py" % (archivo_a_ejecutar))

            ## Intenta ejecutar el script como un programa de pilas.
            try:
                directorio_juego = os.path.dirname(archivo_a_ejecutar)

                if directorio_juego:
                    os.chdir(directorio_juego)

                sys.exit(execfile(archivo_a_ejecutar))
            except Exception as e:
                mostrar_mensaje_de_error_y_salir(e.__class__.name + ": " + e.message)
                return

        if opciones.interprete:
            import pilas
            app = pilas.abrir_interprete(do_raise=True, con_aplicacion=True)
            app.exec_()
            return
        elif opciones.test:
            realizar_pruebas()
        elif opciones.interprete:
            import pilas
            pilas.abrir_interprete(do_raise=True, con_aplicacion=True)
        elif opciones.version:
            from pilas import pilasversion
            print(pilasversion.VERSION)
        else:
            import pilas
            pilas.abrir_asistente()
            
def distancia_entre_radios_de_colision_de_dos_actores(a, b):
    """Retorna la distancia entre dos actores tenieno en cuenta su radio de colisión
    
    :param a: Un actor.
    :param b: El segundo actor a verificar.
    """
    return distancia_entre_dos_actores(a, b) - (a.radio_de_colision + b.radio_de_colision)

def beep(freq, seconds):
    import pygame
    import math
    import numpy

    size = (1366, 720)
    bits = 16

        
    #pyg ame.mixer.pre_init(44100, -bits, 1)#esto hace q se configure en mono, falta ver que el array buf sea unidimensional
    pygame.mixer.pre_init(44100, -bits, 2)#esto hace q se configure en mono, falta ver que el array buf sea unidimensional
    pygame.init()
    #_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    #this sounds totally different coming out of a laptop versus coming out of headphones

    sample_rate = 44100   
    n_samples = int(round(seconds*sample_rate))
    
    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(bits - 1) - 1
    
    for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds
        
        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*freq*t)))        # left
        buf[s][1] = int(round(max_sample*math.sin(2*math.pi*freq*t)))        # left

    sound = pygame.sndarray.make_sound(buf)
    #play once, then loop forever
    sound.play()
    
    def hacerEvent():
        for event in pygame.event.get():
            pass
 
    pilas.escena_actual().tareas.una_vez(0.1, hacerEvent)

                            
