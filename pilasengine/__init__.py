# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import sys
import os
import datetime
import traceback
import random
import signal
import imp
import time
import colores

from PyQt4 import QtGui
from PyQt4 import QtCore

import configuracion
import etiquetas
import escenas
import imagenes
import actores
import utils
import fondos
import depurador
import musica
import interfaz
import sonidos
import habilidades
import comportamientos
import eventos
import controles
import pad
import watcher
import plugins
import simbolos
import datos
import fisica


import widget

VERSION = "1.4.9"


def handler(signum, frame):
    print('Terminando pilas, porque se pulsó ctrl+c.')
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

class Pilas(object):
    """Representa el area de juego de pilas, el componente principal.

    El objeto pilas se inicializa cuando llamamos a la función
    ``pilasengine.iniciar()``. El objeto que se retorna es un
    objeto de esta clase.

    Internamente, este objeto será el que representa la ventana
    principal. Es es contenedor de la escena, el punto de contrucción
    de los actores y quien mantiene con "vida" el juego completo.
    """

    def __init__(self, ancho=640, alto=480, titulo='pilas-engine',
                 con_aceleracion=None, capturar_errores=True,
                 habilitar_mensajes_log=False, x=None, y=None,
                 modo_test=False,
                 pantalla_completa=False, cargar_plugins=False):
        """Inicializa el area de juego con una configuración inicial."""

        self.configuracion = configuracion.Configuracion()
        self.habilitar_mensajes_log(habilitar_mensajes_log)
        self._iniciado_desde_asistente = False
        self.texto_avisar_anterior = None
        self.modo_test = modo_test
        self._audio_inicializado = False

        # Archivo que se observa para hacer livecoding. Esta
        # variable toma valor cuando se llama a la función
        # "pilas.reiniciar_si_cambia(archivo)"
        self.archivo_a_observar = None


        self.log("Iniciando pilas con los parametros", str({"ancho": ancho,
                                                            "alto": alto,
                                                            "titulo": titulo,
                                                            "con_aceleracion": con_aceleracion,
                                                            "capturar_errores": capturar_errores,
                                                            "habilitar_mensajes_log": habilitar_mensajes_log,
                                                            "x": x,
                                                            "y": y}))
        if QtGui.QApplication.instance():
            self.app = QtGui.QApplication.instance()
            self._necesita_ejecutar_loop = False
            self.log("Obteniendo instancia a la aplicacion QT (no se re-genero el objeto de aplicacion)")
        else:
            self.app = QtGui.QApplication(sys.argv)
            self._necesita_ejecutar_loop = True
            self.log("Creando un objeto de aplicacion QT (porque no estaba inicializado)")

        self.widget = None
        self.reiniciar(ancho, alto, titulo, con_aceleracion,
                       habilitar_mensajes_log, x, y, capturar_errores, pantalla_completa)

        if self.configuracion.audio_habilitado():
            self.log("El sistema de audio esta habilitado desde la configuración")
            self._inicializar_audio()
        else:
            self.log("Evitando inicializar el sistema de audio (deshabilitado desde configuración)")

        # Solo re-define el icono cuando se usa pygame, porque
        # sino pygame pone su icono en la ventana.
        if self.configuracion.audio_habilitado():
            self._definir_icono_de_ventana()

        if cargar_plugins:
            self.complementos = plugins.Complementos(self)
        else:
            self.complementos = []

        self._usar_esc_para_alternar_pantalla_completa = True

    def debe_alternar_pantalla_completa_con_esc(self):
        return self._usar_esc_para_alternar_pantalla_completa

    def deshabilitar_alternado_de_pantalla_completa_con_esc(self, deshabilitar):
        self._usar_esc_para_alternar_pantalla_completa = not deshabilitar

    def _definir_icono_de_ventana(self):
        self.log("Definiendo el icono de la ventana")
        try:
            import pygame
            try:
                img = pygame.image.load(self.obtener_ruta_al_recurso('icono.ico'))
                pygame.display.set_icon(img)
            except pygame.error:
                pass
        except ImportError:
            self.log("Imposible cambiar el icono, parece que pygame no esta instalado...")
            pass


    def _inicializar_audio(self):
        self._audio_inicializado = True
        self.log("Inicializando el sistema de audio con pygame")
        import pygame
        pygame.init()
        pygame.mixer.init()

    def forzar_habilitacion_de_audio(self):
        if self._audio_inicializado:
            print("El audio ya ha sido inicializado")
        else:
            self._inicializar_audio()
            self.configuracion.definir_audio_habilitado(True)

    def reiniciar(self, ancho=640, alto=480, titulo='pilas-engine',
                  con_aceleracion=None, habilitar_mensajes_log=False,
                  x=None, y=None, capturar_errores=True,
                  pantalla_completa=False):
        """Genera nuevamente la ventana del videojuego."""

        # Si no especifica usar aceleracion de video, toma la
        # preferencia desde el archivo de configuración.
        if con_aceleracion == None:
            con_aceleracion = self.configuracion.aceleracion_habilitada()
            self.log("No se especificó aceleración de video, así que se adopta la preferencia desde la configuración: con_aceleracion=" + str(con_aceleracion))
        else:
            self.log("Se usa el parametro aceleracion=" + str(con_aceleracion))

        self.habilitar_mensajes_log(habilitar_mensajes_log)
        self.log("Iniciando pilas con una ventana de ", ancho, "x", alto)
        self.log("Reiniciando pilas con los parametros", str({"ancho": ancho,
                                                    "alto": alto,
                                                    "titulo": titulo,
                                                    "con_aceleracion": con_aceleracion,
                                                    "capturar_errores": capturar_errores,
                                                    "habilitar_mensajes_log": habilitar_mensajes_log,
                                                    "x": x,
                                                    "y": y}))
        self.actores = actores.Actores(self)
        self.actores.eliminar_actores_personalizados()
        self.eventos = eventos.Eventos(self)
        self.evento = self.eventos
        self.datos = datos.Datos(self)

        self.controles = controles.Controles(self)
        self.simbolos = simbolos.Simbolos(self)

        if not getattr(self, 'escenas', None):
            self.escenas = escenas.Escenas(self)

        self.escenas.eliminar_escenas_personalizadas()
        self.imagenes = imagenes.Imagenes(self)
        self.utils = utils.Utils(self)
        self.fondos = fondos.Fondos(self)
        self.colores = colores
        self.interfaz = interfaz.Interfaz(self)
        self._capturar_errores = capturar_errores

        if not getattr(self, 'depurador', None):
            self.depurador = depurador.Depurador(self)

        #if not self.configuracion.audio_habilitado():
        #    print "Nota: Iniciando con el sistema de audio deshabitado."

        self.musica = musica.Musica(self)
        self.sonidos = sonidos.Sonidos(self)

        if self.configuracion.pad_habilitado():
            self.pad = pad.Pad(self)
        else:
            self.pad = pad.PadDeshabilitado(self)

        self.habilidades = habilidades.Habilidades()

        es_reinicio = self.widget is not None

        if es_reinicio:
            self.log("Es un reinicio real (ya existia el objeto widget)")
        else:
            self.log("El reinicio se hace por primera vez (es una inicializacion en realidad)")

        if self._iniciado_desde_asistente and es_reinicio:
            parent = self._eliminar_el_anterior_widget()

        if con_aceleracion:
            self.log("Creando el widget canvas con aceleracion de video")
            self.widget = widget.WidgetConAceleracion(self, titulo, ancho, alto,
                                                      self._capturar_errores)
        else:
            self.log("Creando el widget canvas SIN aceleracion de video")
            self.widget = widget.WidgetSinAceleracion(self, titulo, ancho, alto,
                                                      self._capturar_errores)

        if self._iniciado_desde_asistente and es_reinicio:
            self._vincular_el_nuevo_widget(parent)

        self.widget.pantalla_completa = pantalla_completa

        self.escenas.Normal()

        self.comportamientos = comportamientos.Comportamientos()
        self._x = x
        self._y = y

    def esta_en_pantalla_completa(self):
        return self.widget.pantalla_completa

    def ancho(self):
        return self.widget.width()

    def alto(self):
        return self.widget.height()


    def reiniciar_si_cambia(self, archivo):
        """Regista un archivo para hacer livecoding.

        Livecoding es un modo de pilas que se reinicia automáticamente
        si el archivo indicado cambia. Esto de termina programar
        mas rápido y prototipar con mayor fluidez."""

        if not archivo:
            return

        if self.archivo_a_observar:
            raise Exception("Ya se estaba observando un archivo, imposible aceptar esta orden.")

        self.archivo_a_observar = archivo
        self.watcher = watcher.Watcher(archivo, callback=self._reiniciar_pilas_para_livecoding)

    def _reiniciar_pilas_para_livecoding(self):
        """Calback que se ejecuta cuando se detecta modificación de un archivo observado."""
        f = open(self.archivo_a_observar, 'rt')
        contenido = f.read()
        f.close()

        print "%s - Reiniciando" % (time.strftime("%H:%m:%S"))

        geometry = self.widget.geometry()

        scope = {'pilas': self, '__file__': None}
        contenido = self._modificar_codigo_para_reiniciar(contenido)

        try:
            exec(contenido, scope, scope)
        except Exception, e:
            self.procesar_error(e)

        self.widget.setGeometry(geometry)
        self.widget.show()

    def procesar_error(self, e):
        titulo = repr(e)
        descripcion = traceback.format_exc(e)
        escena = self.escenas.Error(titulo, descripcion)
        return escena

    def _modificar_codigo_para_reiniciar(self, contenido):
        import re
        contenido = re.sub('coding\s*:\s*', '', contenido)
        contenido = contenido.replace('pilas = pilasengine.iniciar', 'pilas.reiniciar')
        contenido = contenido.replace('pilas.ejecutar', '#pilas.ejecutar')

        for x in contenido.split('\n'):
            if 'import ' in x and not 'import pilasengine' in x and not 'from ' in x:
                modulo = x.split(' ')[1]
                contenido = contenido.replace(x, x + '\n' + 'reload(' + modulo + ')\n')

            if "__file__" in x:
                contenido = contenido.replace(x, "# livecoding: " + x + "\n")

        return contenido

    def cerrar(self):
        self._eliminar_el_anterior_widget()

    def definir_escena(self, escena):
        self.escenas.definir_escena(escena)

    def cambiar_escena(self, escena):
        self.definir_escena(escena)

    def definir_iniciado_desde_asistente(self, estado):
        self._iniciado_desde_asistente = estado

    def _eliminar_el_anterior_widget(self):
        """Quita de la ventana el widget utilizado anteriorente.

        Este método se suele utilizar cuando se cambia de resolución
        de pantalla o se re-inicia pilas completamente."""

        self.log("Eliminando el widget de canvas principal")
        parent = self.widget.parent()

        if parent:
            parent.removeWidget(self.widget)

        self.widget.setParent(None)
        self.widget.deleteLater()
        self.widget = None

        return parent

    def _vincular_el_nuevo_widget(self, parent):
        """Comienza a mostrar el nuevo widget en pantalla.

        Este método se utiliza para mostrar nuevamente el area de
        juego después de haber cambiado de resolución o reiniciado
        pilas."""
        if parent:
            self.log("Vinculando el widget canvas al layout")
            parent.addWidget(self.widget)
            parent.setCurrentWidget(self.widget)


    def usa_aceleracion(self):
        """Informa si está habilitado el modo aceleración de video."""
        return self.widget.usa_aceleracion_de_video()

    def obtener_widget(self):
        """Retorna el widget en donde se dibuja el juego completo.

        El 'widget' es un componente de la interfaz de usuario, que
        en nuestro caso contiene toda el area de juego."""
        return self.widget

    def obtener_centro_fisico(self):
        """Retorna el centro de la ventana en pixels."""
        return self.widget.obtener_centro_fisico()

    def obtener_coordenada_de_pantalla_relativa(self, x, y):
        """Convierte una coordenada pantalla en una coordenada de común.

        Las coordenadas comunes son las que utilizamos en pilas, donde
        el centro de pantalla es el punto (0, 0). Las coordenadas
        de pantalla, en cambio, son las que tienen como punto (0, 0)
        la esquina superir izquierda de la pantalla.
        """
        dx, dy = self.widget.obtener_centro_fisico()
        return (x - dx, (y - dy) * -1)

    def obtener_coordenada_de_pantalla_absoluta(self, x, y):
        """Convierte una coordenada común en una coordenada de pantalla.

        Las coordenadas comunes son las que utilizamos en pilas, donde
        el centro de pantalla es el punto (0, 0). Las coordenadas
        de pantalla, en cambio, son las que tienen como punto (0, 0)
        la esquina superir izquierda de la pantalla.
        """
        dx, dy = self.widget.obtener_centro_fisico()
        return (x + dx, dy - y)

    def obtener_area(self):
        """Retorna el tamaño real de la ventana."""
        return self.widget.obtener_area()

    def habilitar_mensajes_log(self, estado):
        self._imprimir_mensajes_log = estado

    def obtener_escena_actual(self):
        """Retorna la escena actual."""
        return self.escenas.obtener_escena_actual()

    def escena_actual(self):
        """Retorna la escena actual."""
        return self.obtener_escena_actual()

    def realizar_actualizacion_logica(self):
        """Realiza la etapa de actualización lógica."""
        self.escenas.realizar_actualizacion_logica()

    def realizar_actualizacion_logica_en_modo_pausa(self):
        self.escenas.realizar_actualizacion_logica_en_modo_pausa()

    def forzar_actualizacion_de_interpolaciones(self):
        self.escenas.forzar_actualizacion_de_interpolaciones()

    def simular_actualizacion_logica(self):
        """Realiza un TICK o actualización forzada de lógica.

        Este método es casi interno, se llama desde la batería de tests,
        donde no podemos ejecutar pilas de manera tradicional, con una
        ventana o una llamada a pilas.ejecutar.
        """
        self.escenas.simular_actualizacion_logica()

    def realizar_dibujado(self, painter):
        """Realiza la etapa de actualización gráfica."""
        try:
            self.escenas.realizar_dibujado(painter)
            self.depurador.realizar_dibujado(painter)
        except Exception, e:
            if self._capturar_errores:
                self.log("Capturando un error: %s", e)
                self.depurador.desactivar_todos_los_modos()
                e = sys.exc_info()
                titulo = str(e[1])
                descripcion = traceback.format_exception(e[0], e[1], e[2])
                descripcion = '\n'.join(descripcion)
                _ = self.escenas.Error(titulo, descripcion)
                traceback.print_exc()
            else:
                self.log("Capturando un error: %s", e)
                traceback.print_exc()
                sys.exit(1)

    def log(self, *mensaje):
        """Muestra un mensaje de prueba sobre la consola."""

        if self._imprimir_mensajes_log:
            hora = datetime.datetime.now().strftime("%H:%M:%S")
            mensaje = map(lambda x: str(x), mensaje)
            print(":: %s :: %s " % (hora, " ".join(mensaje)))

    def obtener_ruta_al_recurso(self, ruta):
        """Busca la ruta a un archivo de recursos.

        Los archivos de recursos (como las imagenes) se buscan en varios
        directorios (ver docstring de image.load), así que esta
        función intentará dar con el archivo en cuestión.

        :param ruta: Ruta al archivo (recurso) a inspeccionar.
        """
        self.log("Buscando ruta al recurso:", ruta)
        return utils.obtener_ruta_al_recurso(ruta)

    def ejecutar(self):
        """Muestra la ventana y mantiene el programa en ejecución."""
        if not self._iniciado_desde_asistente:
            if self.widget.pantalla_completa:
                self.widget.showFullScreen()
            else:
                self.widget.show()
                self.widget.raise_()

                self.widget.definir_tamano_real()

                if self._x and self._y:
                    self.widget.move(self._x, self._y)
                else:
                    self.widget.centrar()

        # Inicializa el bucle de pyqt solo si es necesario.
        if self._necesita_ejecutar_loop:
            self.app.exec_()

    def terminar(self):
        self.widget.close()

    def avisar(self, texto):
        if self.texto_avisar_anterior and not self.texto_avisar_anterior.esta_eliminado():
            self.texto_avisar_anterior.eliminar()

        self.texto_avisar_anterior = self.actores.TextoInferior(texto)

    def ocultar_puntero_del_mouse(self):
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))

    def mostrar_puntero_del_mouse(self):
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def obtener_posicion_del_mouse(self):
        return (self.widget.mouse_x, self.widget.mouse_y)

    def obtener_camara(self):
        return self.escena_actual().camara

    def obtener_tareas(self):
        return self.escena_actual().tareas

    def obtener_fisica(self):
        return self.escena_actual().fisica

    def obtener_colisiones(self):
        return self.escena_actual().colisiones

    def obtener_control(self):
        return self.escena_actual().control

    def obtener_actores_en(self, x, y):
        return self.escena_actual().obtener_actores_en(x, y)

    def azar(self, a, b):
        """Retorna un número al azar entre `a` y `b`"""
        return random.randint(a, b)

    def ver(self, objeto):
        """Imprime en pantalla el codigo fuente asociado a un objeto.

        :param objeto: El objeto que se quiere inspeccionar.
        """
        import inspect

        try:
            codigo = inspect.getsource(objeto.__class__)
        except TypeError:
            try:
                codigo = inspect.getsource(objeto)
            except TypeError:
                codigo = "<< imposible inspeccionar código para mostrar >>"

        print codigo

    def definir_pantalla_completa(self, estado):
        if estado:
            self.widget.definir_modo_pantalla_completa()
        else:
            self.widget.definir_modo_ventana()

    def obtener_actor_por_indice(self, indice):
        return self.escena._actores.obtener_actores()[indice]

    def deshabilitar_musica(self, estado=True):
        if estado:
            self.musica.deshabilitar()
        else:
            self.musica.habilitar()

    def deshabilitar_sonido(self, estado=True):
        if estado:
            self.sonidos.deshabilitar()
        else:
            self.sonidos.habilitar()


    control = property(obtener_control, doc="Obtiene el modulo de control")
    tareas = property(obtener_tareas, doc="Obtiene el modulo de tareas")
    camara = property(obtener_camara, doc="Cámara de la escena actual")
    escena = property(obtener_escena_actual, doc="Escena actual")
    fisica = property(obtener_fisica, doc="Retorna el componente fisica")
    colisiones = property(obtener_colisiones, doc="Retorna las colisiones de la escena")


def iniciar(ancho=640, alto=480, titulo='pilas-engine', capturar_errores=True,
            habilitar_mensajes_log=False, con_aceleracion=None, x=None, y=None,
            modo_test=False,
            pantalla_completa=False, cargar_plugins=False):
    """
    Inicia la ventana principal del juego con algunos detalles de funcionamiento.

    Ejemplo de invocación:

        >>> pilas.iniciar(ancho=320, alto=240)

    .. image:: ../../pilas/data/manual/imagenes/iniciar_320_240.png

    :rtype: Pilas

    Parámetros:

    :ancho: el tamaño en pixels para la ventana.
    :alto: el tamaño en pixels para la ventana.
    :titulo: el titulo a mostrar en la ventana.
    :modo_test: subrimer todo mensaje de error por consola, pensado para el lanzador de test automático.
    :capturar_errores: True indica que los errores se tienen que mostrar en la
                       ventana de pilas. En caso de poner False los errores
                       se muestran en consola.
    :habilitar_mensajes_log: Muestra cada operación que hace pilas en consola.
    :con_aceleracion: Indica si se habilita o no la aceleracion de video. Por omisión se trata de obtener la preferencia desde la configuración de pilas.
    :cargar_plugins: Parametro de tipo booleano. Si es True, se cargan todos los plugins que se encuentren dentro del directorio
                     de plugins de pilas.
    """

    pilas = Pilas(ancho=ancho, alto=alto, titulo=titulo,
                  capturar_errores=capturar_errores, x=x, y=y,
                  habilitar_mensajes_log=habilitar_mensajes_log,
                  con_aceleracion=con_aceleracion,
                  pantalla_completa=pantalla_completa,
                  modo_test=modo_test,
                  cargar_plugins=cargar_plugins)
    return pilas


def abrir_asistente():
    import asistente
    return asistente.abrir()

def abrir_manual():
    import manual
    return manual.abrir()

def abrir_api():
    import api
    return api.abrir()

def abrir_configuracion(parent=None):
    import configuracion
    return configuracion.abrir(parent)

def abrir_interprete():
    import interprete
    return interprete.abrir()

def abrir_editor():
    import interprete
    return interprete.abrir_editor()

def abrir_script_con_livereload(archivo):
    import interprete
    ruta = os.path.dirname(archivo)
    ruta = os.path.abspath(ruta)

    return interprete.abrir_script_con_livereload(archivo)




def abrir_script(archivo):

    def terminar_con_error(mensaje):
        _ = QtGui.QApplication(sys.argv)
        error = QtGui.QMessageBox()
        error.critical(None, "Uh, algo anda mal...", mensaje)
        sys.exit(1)

    def ejecutar_archivo(nombre):
        try:
            imp.load_source("__main__", nombre)
        except Exception, e:
            terminar_con_error("Error al ejecutar " + nombre + ":\n" + str(e))

    ruta_absoluta_al_archivo = os.path.abspath(archivo)
    ruta = os.path.dirname(ruta_absoluta_al_archivo)
    os.chdir(ruta)
    ejecutar_archivo(ruta_absoluta_al_archivo)
