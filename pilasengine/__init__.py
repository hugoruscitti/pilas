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
from PyQt4 import QtGui
from PyQt4 import QtCore
import traceback
import random

from pilasengine import escenas
from pilasengine import imagenes
from pilasengine import colores
from pilasengine import actores
from pilasengine import utils
from pilasengine import fondos
from pilasengine import depurador
from pilasengine import musica
from pilasengine import interfaz
from pilasengine import sonidos
from pilasengine import habilidades
from pilasengine import comportamientos
from pilasengine import eventos
from pilasengine import controles
from pilasengine import configuracion

import widget

VERSION = "0.90"


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
                 con_aceleracion=True, capturar_errores=True,
                 habilitar_mensajes_log=False, x=None, y=None):
        """Inicializa el area de juego con una configuración inicial."""
        self._iniciado_desde_asistente = False
        self.texto_avisar_anterior = None

        if QtGui.QApplication.instance():
            self.app = QtGui.QApplication.instance()
            self._necesita_ejecutar_loop = False
        else:
            self.app = QtGui.QApplication(sys.argv)
            self._necesita_ejecutar_loop = True

        self.widget = None
        self.reiniciar(ancho, alto, titulo, con_aceleracion,
                       habilitar_mensajes_log, x, y, capturar_errores)

        if configuracion.AUDIO_HABILITADO:
            self._inicializar_audio()

    def _inicializar_audio(self):
        import pygame
        pygame.mixer.init()

    def reiniciar(self, ancho=640, alto=480, titulo='pilas-engine',
                  con_aceleracion=True, habilitar_mensajes_log=False,
                  x=None, y=None, capturar_errores=True):
        """Genera nuevamente la ventana del videojuego."""
        self.habilitar_mensajes_log(habilitar_mensajes_log)
        self.log("Iniciando pilas con una ventana de ", ancho, "x", alto)
        self.actores = actores.Actores(self)
        self.actores.eliminar_actores_personalizados()
        self.eventos = eventos.Eventos(self)
        self.control = controles.Controles(self)
        self.escenas = escenas.Escenas(self)
        self.imagenes = imagenes.Imagenes(self)
        self.utils = utils.Utils(self)
        self.fondos = fondos.Fondos(self)
        self.colores = colores
        self.interfaz = interfaz.Interfaz(self)
        self._capturar_errores = capturar_errores

        if not getattr(self, 'depurador', None):
            self.depurador = depurador.Depurador(self)

        self.musica = musica.Musica(self)
        self.sonidos = sonidos.Sonidos(self)
        self.habilidades = habilidades.Habilidades()
        self.comportamientos = comportamientos.Comportamientos()

        es_reinicio = self.widget is not None

        if self._iniciado_desde_asistente and es_reinicio:
            parent = self._eliminar_el_anterior_widget()

        if con_aceleracion:
            self.widget = widget.WidgetConAceleracion(self, titulo, ancho, alto,
                                                      self._capturar_errores)
        else:
            self.widget = widget.WidgetSinAceleracion(self, titulo, ancho, alto,
                                                      self._capturar_errores)

        if self._iniciado_desde_asistente and es_reinicio:
            self._vincular_el_nuevo_widget(parent)

        self.escenas.Normal()
        self._x = x
        self._y = y

    def definir_iniciado_desde_asistente(self, estado):
        self._iniciado_desde_asistente = estado

    def _eliminar_el_anterior_widget(self):
        """Quita de la ventana el widget utilizado anteriorente.

        Este método se suele utilizar cuando se cambia de resolución
        de pantalla o se re-inicia pilas completamente."""
        parent = self.widget.parent()

        if parent:
            parent.removeWidget(self.widget)

        self.widget.setParent(None)
        return parent

    def _vincular_el_nuevo_widget(self, parent):
        """Comienza a mostrar el nuevo widget en pantalla.

        Este método se utiliza para mostrar nuevamente el area de
        juego después de haber cambiado de resolución o reiniciado
        pilas."""
        if parent:
            parent.addWidget(self.widget)
            parent.setCurrentWidget(self.widget)

    def usa_aceleracion(self):
        """Informa si está habilitado el modo aceleración de video."""
        return (self.widget.__class__ == widget.WidgetConAceleracion)

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
            self.widget.show()
            self.widget.raise_()
            self.widget.definir_tamano_real()

            if self._x and self._y:
                self.widget.move(self._x, self._y)

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

    def obtener_camara(self):
        return self.escena_actual().camara

    def obtener_tareas(self):
        return self.escena_actual().tareas

    def obtener_fisica(self):
        return self.escena_actual().fisica

    def obtener_colisiones(self):
        return self.escena_actual().colisiones

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

    tareas = property(obtener_tareas, doc="Obtiene el modulo de tareas")
    camara = property(obtener_camara, doc="Cámara de la escena actual")
    escena = property(obtener_escena_actual, doc="Escena actual")
    fisica = property(obtener_fisica, doc="Retorna el componente fisica")
    colisiones = property(obtener_colisiones, doc="Retorna las colisiones de la escena")


def iniciar(ancho=640, alto=480, titulo='pilas-engine', capturar_errores=True,
            habilitar_mensajes_log=False, x=None, y=None):
    """
    Inicia la ventana principal del juego con algunos detalles de funcionamiento.

    Ejemplo de invocación:

        >>> pilas.iniciar(ancho=320, alto=240)

    .. image:: images/iniciar_320_240.png

    Parámetros:

    :ancho: el tamaño en pixels para la ventana.
    :alto: el tamaño en pixels para la ventana.
    :titulo: el titulo a mostrar en la ventana.
    :capturar_errores: True indica que los errores se tienen que mostrar en la
                       ventana de pilas. En caso de poner False los errores
                       se muestran en consola.
    :habilitar_mensajes_log: Muestra cada operación que hace pilas en consola.
    """
    pilas = Pilas(ancho=ancho, alto=alto, titulo=titulo,
                  capturar_errores=capturar_errores, x=x, y=y)
    return pilas


def abrir_asistente():
    import asistente
    return asistente.abrir()


def abrir_manual():
    import manual
    return manual.abrir()


def abrir_interprete():
    import interprete
    return interprete.abrir()


def abrir_script_con_livereload(archivo):
    import interprete
    ruta = os.path.dirname(archivo)
    ruta = os.path.abspath(ruta)

    return interprete.abrir_script_con_livereload(archivo)
