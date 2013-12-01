# -*- coding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtOpenGL import QGLWidget
from PyQt4.QtGui import QWidget
from pilas import actores, colores, depurador, eventos, fps
from pilas import imagenes, simbolos, utils
from pilas import dev
from pilas.widget_log import WidgetLog
import os
import pilas
import sys
import traceback
import copy
import math


class LibreriaImagenes(object):
    """ Clase que permite cachear las imagenes cargadas en el juego."""
    def __init__(self):
        # Diccionario donde se guardaran las imagenes y sus referencias.
        self._imagenes = dict()

    def agregar_imagen(self, imagen):
        """ Permite agregar una imagen a la cache.

        :param imagen: Objeto Imagen a almacenar.
        :type imagen: Imagen
        """

        # Si la imagen no se encuentra cacheada se almacena.
        # El campo ruta_original del objeto Imagen es el indice por el que se
        # buscará en la caché de imágenes.
        if not(imagen.ruta_original in self._imagenes):
            self._imagenes[imagen.ruta_original] = imagen

        return imagen.ruta_original

    def obtener_imagen(self, indice):
        """ Obtiene una imagen de la cache.
        De no encontrarse, devuelve una imagen estandar. """
        try:
            return self._imagenes[indice]
        except:
            return imagenes.cargar("sin_imagen.png")

    def tiene(self, indice):
        """ Comprueba si una imagen está cacheada.

        :param indice: Nombre del indice de la imagen a buscar.
        :type indice: string

        """
        return indice in self._imagenes

    def obtener_cantidad(self):
        return len(self._imagenes)


class Ventana(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setStyleSheet("QWidget {background-color : #222}")

    def set_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.setParent(self)

    def resizeEvent(self, event):
        self.canvas.resize_to(self.width(), self.height())


class CanvasWidgetAbstracto(object):

    def __init__(self, motor, ancho, alto, gestor_escenas, permitir_depuracion,
                 rendimiento):
        QGLWidget.__init__(self, None)

        self.painter = QtGui.QPainter()

        self.pausa_habilitada = False

        self.setMouseTracking(True)
        self.mouse_x = 0
        self.mouse_y = 0

        self.motor = motor

        self.fps = fps.FPS(rendimiento, True)

        if permitir_depuracion:
            self.depurador = depurador.Depurador(motor.obtener_lienzo(), self.fps)
        else:
            self.depurador = depurador.DepuradorDeshabilitado()

        self.original_width = ancho
        self.original_height = alto

        self.escala = 1

        self.startTimer(1000/100.0)

        self.gestor_escenas = gestor_escenas

    def resize_to(self, w, h):
        escala_x = w / float(self.original_width)
        escala_y = h / float(self.original_height)
        escala = min(escala_x, escala_y)

        final_w = self.original_width * escala
        final_h = self.original_height * escala
        self.escala = escala

        x = w - final_w
        y = h - final_h

        self.setGeometry(x/2, y/2, final_w, final_h)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.scale(self.escala, self.escala)

        self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self.gestor_escenas.escena_actual():
            if not(self.gestor_escenas.escena_actual().escena_pausa):
                self.painter.fillRect(0, 0, self.original_width, self.original_height, QtGui.QColor(128, 128, 128))
        self.depurador.comienza_dibujado(self.motor, self.painter)

        if self.gestor_escenas.escena_actual():
            actores_de_la_escena = self.gestor_escenas.escena_actual().actores
            for actor in actores_de_la_escena:
                try:
                    if not actor.esta_fuera_de_la_pantalla():
                        actor.dibujar(self.painter)
                except Exception:
                    print traceback.format_exc()
                    print sys.exc_info()[0]
                    actor.eliminar()

                self.depurador.dibuja_al_actor(self.motor, self.painter, actor)

        self.depurador.termina_dibujado(self.motor, self.painter)
        self.painter.end()

    def save_to_disk(self, filename):
        try:
            image =  QtGui.QPixmap(self.width(), self.height())
            image = QtGui.QPixmap.grabWidget(self, 0, 0, self.width(), self.height())
            if not image.save(filename, "PNG", -1):
                print "Imposible guardar la captura de pantalla."
        except Exception:
            print traceback.format_exc()
            print sys.exc_info()[0]

    def timerEvent(self, event):
        try:
            self._realizar_actualizacion_logica()
        except Exception:
            print traceback.format_exc()
            print sys.exc_info()[0]

        self.update()

    def _realizar_actualizacion_logica(self):
        for x in range(self.fps.actualizar()):
            if not self.pausa_habilitada:
                self._actualizar_eventos_y_actores()
                self._actualizar_escena()

    def _actualizar_escena(self):
        self.gestor_escenas.actualizar()

    def _actualizar_eventos_y_actores(self):
        eventos.actualizar.emitir()

        try:
            for actor in self.gestor_escenas.escena_actual().actores:
                actor.pre_actualizar()
                actor.actualizar()
        except Exception:
            print traceback.format_exc()
            print sys.exc_info()[0]

    def mouseMoveEvent(self, e):
        escala = self.escala
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x()/escala, e.pos().y()/escala)

        izquierda, derecha, arriba, abajo = utils.obtener_bordes()

        x += pilas.mundo.motor.camara_x
        y += pilas.mundo.motor.camara_y

        dx, dy = x - self.mouse_x, y - self.mouse_y

        self.gestor_escenas.escena_actual().mueve_mouse.emitir(x=x, y=y, dx=dx, dy=dy)

        self.mouse_x = x
        self.mouse_y = y
        self.depurador.cuando_mueve_el_mouse(x, y)

    def keyPressEvent(self, event):
        codigo_de_tecla = self._obtener_codigo_de_tecla_normalizado(event.key())

        # Se mantiene este lanzador de eventos por la clase Control
        if event.key() == QtCore.Qt.Key_Escape:
            eventos.pulsa_tecla_escape.emitir()
        if event.key() == QtCore.Qt.Key_P and event.modifiers() == QtCore.Qt.AltModifier:
            self.alternar_pausa()
        if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.AltModifier:
            self.alternar_pantalla_completa()

        eventos.pulsa_tecla.emitir(codigo=codigo_de_tecla, es_repeticion=event.isAutoRepeat(), texto=event.text())
        self.depurador.cuando_pulsa_tecla(codigo_de_tecla, event.text())

    def keyReleaseEvent(self, event):
        codigo_de_tecla = self._obtener_codigo_de_tecla_normalizado(event.key())
        # Se mantiene este lanzador de eventos por la clase Control
        eventos.suelta_tecla.emitir(codigo=codigo_de_tecla, es_repeticion=event.isAutoRepeat(), texto=event.text())

    def wheelEvent(self, e):
        self.gestor_escenas.escena_actual().mueve_rueda.emitir(delta=e.delta() / 120)

    def mousePressEvent(self, e):
        escala = self.escala
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x()/escala, e.pos().y()/escala)
        boton_pulsado = e.button()

        x += pilas.mundo.motor.camara_x
        y += pilas.mundo.motor.camara_y

        self.gestor_escenas.escena_actual().click_de_mouse.emitir(x=x, y=y, dx=0, dy=0, boton=boton_pulsado)

    def mouseReleaseEvent(self, e):
        escala = self.escala
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x()/escala, e.pos().y()/escala)
        boton_pulsado = e.button()

        x += pilas.mundo.motor.camara_x
        y += pilas.mundo.motor.camara_y

        self.gestor_escenas.escena_actual().termina_click.emitir(x=x, y=y, dx=0, dy=0, boton=boton_pulsado)

    def _obtener_codigo_de_tecla_normalizado(self, tecla_qt):
        teclas = {
            QtCore.Qt.Key_Left: simbolos.IZQUIERDA,
            QtCore.Qt.Key_Right: simbolos.DERECHA,
            QtCore.Qt.Key_Up: simbolos.ARRIBA,
            QtCore.Qt.Key_Down: simbolos.ABAJO,
            QtCore.Qt.Key_Space: simbolos.ESPACIO,
            QtCore.Qt.Key_Return: simbolos.SELECCION,
            QtCore.Qt.Key_F1: simbolos.F1,
            QtCore.Qt.Key_F2: simbolos.F2,
            QtCore.Qt.Key_F3: simbolos.F3,
            QtCore.Qt.Key_F4: simbolos.F4,
            QtCore.Qt.Key_F5: simbolos.F5,
            QtCore.Qt.Key_F6: simbolos.F6,
            QtCore.Qt.Key_F7: simbolos.F7,
            QtCore.Qt.Key_F8: simbolos.F8,
            QtCore.Qt.Key_F9: simbolos.F9,
            QtCore.Qt.Key_F10: simbolos.F10,
            QtCore.Qt.Key_F11: simbolos.F11,
            QtCore.Qt.Key_F12: simbolos.F12,
            QtCore.Qt.Key_A: simbolos.a,
            QtCore.Qt.Key_B: simbolos.b,
            QtCore.Qt.Key_C: simbolos.c,
            QtCore.Qt.Key_D: simbolos.d,
            QtCore.Qt.Key_E: simbolos.e,
            QtCore.Qt.Key_F: simbolos.f,
            QtCore.Qt.Key_G: simbolos.g,
            QtCore.Qt.Key_H: simbolos.h,
            QtCore.Qt.Key_I: simbolos.i,
            QtCore.Qt.Key_J: simbolos.j,
            QtCore.Qt.Key_K: simbolos.k,
            QtCore.Qt.Key_L: simbolos.l,
            QtCore.Qt.Key_M: simbolos.m,
            QtCore.Qt.Key_N: simbolos.n,
            QtCore.Qt.Key_O: simbolos.o,
            QtCore.Qt.Key_P: simbolos.p,
            QtCore.Qt.Key_Q: simbolos.q,
            QtCore.Qt.Key_R: simbolos.r,
            QtCore.Qt.Key_S: simbolos.s,
            QtCore.Qt.Key_T: simbolos.t,
            QtCore.Qt.Key_U: simbolos.u,
            QtCore.Qt.Key_V: simbolos.v,
            QtCore.Qt.Key_W: simbolos.w,
            QtCore.Qt.Key_X: simbolos.x,
            QtCore.Qt.Key_Y: simbolos.y,
            QtCore.Qt.Key_Z: simbolos.z,
        }

        if teclas.has_key(tecla_qt):
            return teclas[tecla_qt]
        else:
            return tecla_qt

    def pantalla_completa(self):
        self.motor.ventana.showFullScreen()

    def pantalla_modo_ventana(self):
        self.motor.ventana.showNormal()

    def esta_en_pantalla_completa(self):
        return self.motor.ventana.isFullScreen()

    def alternar_pausa(self):
        if self.pausa_habilitada:
            self.pausa_habilitada = False
            self.actor_pausa.eliminar()
            eventos.pulsa_tecla.desconectar_por_id('tecla_en_pausa')
        else:
            self.pausa_habilitada = True
            self.actor_pausa = actores.Pausa()
            self.actor_pausa.fijo = True
            self.id_evento = eventos.pulsa_tecla.conectar(self.avanzar_un_solo_cuadro_de_animacion, id='tecla_en_pausa')

    def avanzar_un_solo_cuadro_de_animacion(self, evento):
        self._actualizar_eventos_y_actores()

    def alternar_pantalla_completa(self):
        """Permite cambiar el modo de video.

        Si está en modo ventana, pasa a pantalla completa y viceversa.
        """
        if self.esta_en_pantalla_completa():
            self.pantalla_modo_ventana()
        else:
            self.pantalla_completa()


class BaseActor(object):

    def __init__(self):
        self._rotacion = 0
        self._transparencia = 0
        self.centro_x = 0
        self.centro_y = 0
        self._escala_x = 1
        self._escala_y = 1
        self._espejado = False
        self.fijo = 0

    def definir_centro(self, x, y):
        self.centro_x = x
        self.centro_y = y

    def obtener_posicion(self):
        return self.x, self.y

    def definir_posicion(self, x, y):
        self.x, self.y = x, y

    def obtener_escala(self):
        return self._escala_x

    def definir_escala(self, s):
        self._escala_x = s
        self._escala_y = s

    def definir_escala_x(self, s):
        self._escala_x = s

    def definir_escala_y(self, s):
        self._escala_y = s

    def definir_transparencia(self, nuevo_valor):
        self._transparencia = nuevo_valor

    def obtener_transparencia(self):
        return self._transparencia

    def obtener_rotacion(self):
        return self._rotacion

    def definir_rotacion(self, r):
        self._rotacion = r

    def set_espejado(self, espejado):
        self._espejado = espejado


class Imagen(object):

    def __init__(self, ruta):
        self.ruta_original = ruta

        if isinstance(ruta, QtGui.QPixmap):
            self._imagen = ruta
        else:
            if ruta.lower().endswith("jpeg") or ruta.lower().endswith("jpg"):
                try:
                    self._imagen = self.cargar_jpeg(ruta)
                except:
                    self._imagen = QtGui.QPixmap(ruta)
            else:
                self._imagen = QtGui.QPixmap(ruta)

        #pilas.mundo.motor.libreria_imagenes.agregar_imagen(self)
        #

    def obtener_recuadro(self, dx, dy, ancho, alto):
        qi = self._imagen.toImage()
        rect = QtCore.QRect(dx, dy, ancho, alto)
        qi = qi.copy(rect)
        return Imagen(QtGui.QPixmap.fromImage(qi))

    def cargar_jpeg(self, ruta):
        from PIL import Image
        import StringIO

        pilImage = Image.open(ruta)
        stringIO = StringIO.StringIO()
        pilImage.save(stringIO, format="png")

        pixmapImage = QtGui.QPixmap()
        pixmapImage.loadFromData(stringIO.getvalue())

        return pixmapImage

    def ancho(self):
        return self._imagen.size().width()

    def alto(self):
        return self._imagen.size().height()

    def centro(self):
        "Retorna una tupla con la coordenada del punto medio del la imagen."
        return (self.ancho()/2, self.alto()/2)

    def avanzar(self):
        pass

    def dibujar(self, painter, x, y, dx=0, dy=0, escala_x=1, escala_y=1, rotacion=0, transparencia=0):
        """Dibuja la imagen sobre la ventana que muestra el motor.

           x, y: indican la posicion dentro del mundo.
           dx, dy: es el punto centro de la imagen (importante para rotaciones).
           escala_x, escala_yindican cambio de tamano (1 significa normal).
           rotacion: angulo de inclinacion en sentido de las agujas del reloj.
        """

        painter.save()
        centro_x, centro_y = pilas.mundo.motor.centro_fisico()
        painter.translate(x + centro_x, centro_y - y)
        painter.rotate(rotacion)
        painter.scale(escala_x, escala_y)

        if transparencia:
            painter.setOpacity(1 - transparencia/100.0)

        self._dibujar_pixmap(painter, -dx, -dy)
        painter.restore()

    def _dibujar_pixmap(self, painter, x, y):
        painter.drawPixmap(x, y, self._imagen)

    def __str__(self):
        nombre_imagen = os.path.basename(self.ruta_original)
        return "<Imagen del archivo '%s'>" % (nombre_imagen)


class CanvasOpenGlWidget(CanvasWidgetAbstracto, QGLWidget):
    pass


class CanvasNormalWidget(CanvasWidgetAbstracto, QWidget):
    pass


class Grilla(Imagen):

    """Representa una grilla regular, que se utiliza en animaciones.

       La grilla regular se tiene que crear indicando la cantidad
       de filas y columnas. Una vez definida se puede usar como
       una imagen normal, solo que tiene dos metodos adicionales
       para ``definir_cuadro`` y ``avanzar`` el cuadro actual.
    """

    def __init__(self, ruta, columnas=1, filas=1):
        Imagen.__init__(self, ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = Imagen.ancho(self) / columnas
        self.cuadro_alto = Imagen.alto(self) / filas
        self.definir_cuadro(0)

    def ancho(self):
        return self.cuadro_ancho

    def alto(self):
        return self.cuadro_alto

    def _dibujar_pixmap(self, painter, x, y):
        painter.drawPixmap(x, y, self._imagen, self.dx, self.dy, self.cuadro_ancho, self.cuadro_alto)

    def definir_cuadro(self, cuadro):
        self._cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        self.dx = frame_col * self.cuadro_ancho
        self.dy = frame_row * self.cuadro_alto

    def avanzar(self):
        ha_avanzado = True
        cuadro_actual = self._cuadro + 1

        if cuadro_actual >= self.cantidad_de_cuadros:
            cuadro_actual = 0
            ha_avanzado = False

        self.definir_cuadro(cuadro_actual)
        return ha_avanzado

    def obtener_cuadro(self):
        return self._cuadro

    def dibujarse_sobre_una_pizarra(self, pizarra, x, y):
        pizarra.pintar_parte_de_imagen(self, self.dx, self.dy, self.cuadro_ancho, self.cuadro_alto, x, y)


class Lienzo(Imagen):

    def __init__(self):
        pass

    def texto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro):
        "Imprime un texto respespetando el desplazamiento de la camara."
        self.texto_absoluto(painter, cadena, x, y, magnitud, fuente, color)

    def texto_absoluto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro):
        "Imprime un texto sin respetar al camara."
        x, y = utils.hacer_coordenada_pantalla_absoluta(x, y)

        r, g, b, a = color.obtener_componentes()
        painter.setPen(QtGui.QColor(r, g, b))

        if fuente:
            nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        else:
            nombre_de_fuente = painter.font().family()

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        painter.setFont(font)
        painter.drawText(x, y, cadena)

    def pintar(self, painter, color):
        r, g, b, a = color.obtener_componentes()
        ancho, alto = pilas.mundo.obtener_area()
        painter.fillRect(0, 0, ancho, alto, QtGui.QColor(r, g, b))

    def linea(self, painter, x0, y0, x1, y1, color=colores.negro, grosor=1):
        x0, y0 = utils.hacer_coordenada_pantalla_absoluta(x0, y0)
        x1, y1 = utils.hacer_coordenada_pantalla_absoluta(x1, y1)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        painter.setPen(pen)
        painter.drawLine(x0, y0, x1, y1)

    def angulo(self, motor, x, y, angulo, radio, color, grosor):
        angulo_en_radianes = math.radians(-angulo)
        dx = math.cos(angulo_en_radianes) * radio
        dy = math.sin(angulo_en_radianes) * radio
        self.linea(motor, x, y, x + dx, y + dy, color, grosor)


    def poligono(self, motor, puntos, color=colores.negro, grosor=1, cerrado=False):
        x, y = puntos[0]
        if cerrado:
            puntos.append((x, y))

        for p in puntos[1:]:
            nuevo_x, nuevo_y = p
            self.linea(motor, x, y, nuevo_x, nuevo_y, color, grosor)
            x, y = nuevo_x, nuevo_y

    def cruz(self, painter, x, y, color=colores.negro, grosor=1):
        t = 3
        self.linea(painter, x - t, y - t, x + t, y + t, color, grosor)
        self.linea(painter, x + t, y - t, x - t, y + t, color, grosor)

    def circulo(self, painter, x, y, radio, color=colores.negro, grosor=1):
        x, y = utils.hacer_coordenada_pantalla_absoluta(x, y)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        painter.setPen(pen)
        painter.drawEllipse(x-radio, y-radio, radio*2, radio*2)

    def rectangulo(self, painter, x, y, ancho, alto, color=colores.negro, grosor=1):
        x, y = utils.hacer_coordenada_pantalla_absoluta(x, y)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        painter.setPen(pen)
        painter.drawRect(x, y, ancho, alto)


class Superficie(Imagen):

    def __init__(self, ancho, alto):
        self._imagen = QtGui.QPixmap(ancho, alto)
        self._imagen.fill(QtGui.QColor(255, 255, 255, 0))
        self.canvas = QtGui.QPainter()
        self.ruta_original = os.urandom(25)

    def pintar(self, color):
        r, g, b, a = color.obtener_componentes()
        self._imagen.fill(QtGui.QColor(r, g, b, a))

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto, x, y):
        self.canvas.begin(self._imagen)
        self.canvas.drawPixmap(x, y, imagen._imagen, origen_x, origen_y, ancho, alto)
        self.canvas.end()

    def pintar_imagen(self, imagen, x=0, y=0):
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(), imagen.alto(), x, y)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro, ancho=0, vertical=False):
        self.canvas.begin(self._imagen)
        r, g, b, a = color.obtener_componentes()
        self.canvas.setPen(QtGui.QColor(r, g, b))
        dx = x
        dy = y

        if fuente:
            nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        else:
            nombre_de_fuente = self.canvas.font().family()

        if not ancho:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
            ancho = self._imagen.width()
        else:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        self.canvas.setFont(font)
        metrica = QtGui.QFontMetrics(font)


        if vertical:
            lineas = [t for t in cadena]
        else:
            lineas = cadena.split('\n')

        for line in lineas:
            r = QtCore.QRect(dx, dy, ancho, 2000)
            rect = self.canvas.drawText(r, flags, line)
            dy += rect.height()

        self.canvas.end()

    def circulo(self, x, y, radio, color=colores.negro, relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawEllipse(x-radio, y-radio, radio*2, radio*2)
        self.canvas.end()

    def rectangulo(self, x, y, ancho, alto, color=colores.negro, relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawRect(x, y, ancho, alto)
        self.canvas.end()

    def linea(self, x, y, x2, y2, color=colores.negro, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        self.canvas.drawLine(x, y, x2, y2)
        self.canvas.end()

    def poligono(self, puntos, color, grosor, cerrado=False):
        x, y = puntos[0]

        if cerrado:
            puntos.append((x, y))

        for p in puntos[1:]:
            nuevo_x, nuevo_y = p
            self.linea(x, y, nuevo_x, nuevo_y, color, grosor)
            x, y = nuevo_x, nuevo_y

    def dibujar_punto(self, x, y, color=colores.negro):
        self.circulo(x, y, 3, color=color, relleno=True)

    def limpiar(self):
        self._imagen.fill(QtGui.QColor(0, 0, 0, 0))


class Texto(Superficie):
    CACHE_FUENTES = {}

    def __init__(self, texto, magnitud, motor, vertical=False, fuente=None, color=pilas.colores.negro, ancho=None):
        ancho, alto = motor.obtener_area_de_texto(texto, magnitud, vertical, fuente, ancho)
        Superficie.__init__(self, ancho, alto)
        self._ancho_del_texto = ancho
        self.dibujar_texto = self.texto
        self.dibujar_texto(texto, magnitud=magnitud, fuente=fuente, color=color, ancho=ancho, vertical=vertical)
        self.ruta_original = texto.encode('ascii', 'xmlcharrefreplace') + str(os.urandom(25))
        self.texto = texto

    @classmethod
    def cargar_fuente_desde_cache(kclass, fuente_como_ruta):
        """Carga o convierte una fuente para ser utilizada dentro del motor.

        Permite a los usuarios referirse a las fuentes como ruta a archivos, sin
        tener que preocuparse por el font-family.

        :param fuente_como_ruta: Ruta al archivo TTF que se quiere utilizar.

        Ejemplo:

            >>> Texto.cargar_fuente_desde_cache('myttffile.ttf')
            'Visitor TTF1'
        """

        if not fuente_como_ruta in Texto.CACHE_FUENTES.keys():
            ruta_a_la_fuente = pilas.utils.obtener_ruta_al_recurso(fuente_como_ruta)
            fuente_id = QtGui.QFontDatabase.addApplicationFont(ruta_a_la_fuente)
            Texto.CACHE_FUENTES[fuente_como_ruta] = fuente_id
        else:
            fuente_id = Texto.CACHE_FUENTES[fuente_como_ruta]

        return str(QtGui.QFontDatabase.applicationFontFamilies(fuente_id)[0])


class Actor(BaseActor):

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):

        # Si la imagen es una cadena, cargamos la imagen y la cacheamos.
        #if isinstance(imagen, str):
        #    self.indice_imagen = pilas.mundo.motor.libreria_imagenes.agregar_imagen(imagenes.cargar(imagen))
        #else:
        #    # Si en un objeto Imagen lo almacenamos directamente.
        #    self.indice_imagen = pilas.mundo.motor.libreria_imagenes.agregar_imagen(imagen)
        self.imagen = imagen

        self.x = x
        self.y = y
        BaseActor.__init__(self)

    def get_imagen(self):
        """ Obtinene la imagen del Actor. """
        return self.obtener_imagen()

    def set_imagen(self, imagen):
        """ Establece la imagen del actor.

        :param imagen: Imagen que definirá al actor.
        :type imagen: Imagen, Grilla,
        """
        if isinstance(imagen, Grilla):
            self._imagen = copy.copy(imagen)
        elif isinstance(imagen, str):
            self._imagen = pilas.imagenes.cargar(imagen)
        else:
            self._imagen = imagen

        """
        # Comprobamos si el parametro imagen es un objeto Imagen o Grilla.
        if isinstance(imagen, Imagen) or isinstance(imagen, Grilla):
            # Comprobamos si ya está cacheada esa imagen.
            if pilas.mundo.motor.libreria_imagenes.tiene(imagen.ruta_original):
                # Si es así nos guardamos el indice de la imagen en la caché, que corresponde
                # con la ruta de la imagen.
                self.indice_imagen = imagen.ruta_original
            else:
                # Si la imagen no estaba cacheada la guardamos.
                self.indice_imagen = pilas.mundo.motor.libreria_imagenes.agregar_imagen(imagen)
        else:
            # Si el parámetro imagen es un string.
            if isinstance(imagen, str):
                if pilas.mundo.motor.libreria_imagenes.tiene(imagen):
                    self.indice_imagen = imagen
                else:
                    self.indice_imagen = pilas.mundo.motor.libreria_imagenes.agregar_imagen(imagenes.cargar(imagen))
            else:
                raise Exception("Lo siento, solo se admiten rutas a archivos o imagenes.")
        """

    imagen = property(get_imagen, set_imagen, doc="")

    def definir_imagen(self, imagen):
        self.imagen = imagen

    def obtener_imagen(self):
        #return pilas.mundo.motor.libreria_imagenes.obtener_imagen(self.indice_imagen)
        return self._imagen

    def dibujar(self, painter):
        escala_x, escala_y = self._escala_x, self._escala_y

        if self._espejado:
            escala_x *= -1

        if not self.fijo:
            dx = pilas.mundo.motor.camara_x
            dy = pilas.mundo.motor.camara_y
        else:
            dx = 0
            dy = 0

        x = self.x - dx
        y = self.y - dy

        #pilas.mundo.motor.libreria_imagenes.obtener_imagen(self.indice_imagen).dibujar(painter, x, y, self.centro_x, self.centro_y,
        #        escala_x, escala_y, self._rotacion, self._transparencia)
        #self.imagen.dibujar(painter, x, y, self.centro_x, self.centro_y)
        self.imagen.dibujar(painter, x, y, self.centro_x, self.centro_y,
                            escala_x, escala_y, self._rotacion, self._transparencia)


## Backend: audio deshabilitado

class SonidoDeshabilitado:
    deshabilitado = True

    def __init__(self, player, ruta):
        pass

    def reproducir(self, repetir=False):
        pass

    def detener(self):
        pass

    def pausar(self):
        pass

    def continuar(self):
        pass


class MusicaDeshabilitada(SonidoDeshabilitado):

    def __init__(self, media, ruta):
        SonidoDeshabilitado.__init__(self, media, ruta)

## Backend: gstreamer


class SonidoGST:
    deshabilitado = False

    def __init__(self, player, ruta):
        self.ruta = ruta
        self.sonido = player
        self.sonido.set_property('uri', 'file://{}'.format(self.ruta))
        self._repetir = None

    def _play(self):
        import gst
        self.sonido.set_state(gst.STATE_NULL)
        self.sonido.set_state(gst.STATE_PLAYING)

    def reproducir(self, repetir=False):
        import gst
        import pilas
        if not self.deshabilitado:
            self.detener()
            self._play()
            if repetir:
                self.sonido.get_state()
                nanosecs = float(self.sonido.query_duration(gst.FORMAT_TIME)[0])
                duracion = (nanosecs + 10) / gst.SECOND
                self._repetir = pilas.mundo.agregar_tarea_siempre(duracion,
                                                                  self._play)

    def detener(self):
        import gst
        if self._repetir:
            self._repetir.terminar()
            self._repetir = None
        self.sonido.set_state(gst.STATE_NULL)


class MusicaGST(SonidoGST):

    def __init__(self, media, ruta):
        SonidoGST.__init__(self, media, ruta)

## Backend: audio phonon


class SonidoPhonon:
    deshabilitado = False

    def __init__(self, media, ruta):
        from PyQt4 import phonon
        self.media = media
        self.ruta = ruta

        self.source = phonon.Phonon.MediaSource(ruta)
        self.sonido = phonon.Phonon.createPlayer(phonon.Phonon.GameCategory, self.source)

    def _play(self):
        if not self.deshabilitado:
            self.sonido.seek(0)
            self.sonido.play()

    def reproducir(self, repetir=False):
        if not self.deshabilitado:
            if repetir:
                try:
                    self.sonido.finished.disconnect(self._play)
                except TypeError:
                    pass
                self.sonido.finished.connect(self._play)
            else:
                try:
                    self.sonido.finished.disconnect(self._play)
                except TypeError:
                    pass
            self._play()

    def detener(self):
        "Detiene el audio."
        self.sonido.stop()

    def pausar(self):
        "Hace una pausa del audio."
        self.sonido.pause()

    def continuar(self):
        "Continúa reproduciendo el audio."
        if not self.deshabilitado:
            self.sonido.play()


class MusicaPhonon(SonidoPhonon):

    def __init__(self, media, ruta):
        SonidoPhonon.__init__(self, media, ruta)


class SonidoPygame:
    deshabilitado = False

    def __init__(self, media, ruta):
        import pygame
        self.media = media
        self.ruta = ruta
        self.sonido = pygame.mixer.Sound(ruta)

    def _play(self):
        if not self.deshabilitado:
            self.sonido.play()

    def reproducir(self, repetir=False):
        if not self.deshabilitado:
            if repetir:
                self.sonido.play(-1)
            else:
                self.sonido.play()

    def detener(self):
        "Detiene el audio."
        self.sonido.stop()

    def pausar(self):
        "Hace una pausa del audio."
        self.sonido.stop()

    def continuar(self):
        "Continúa reproduciendo el audio."
        if not self.deshabilitado:
            self.sonido.play()

class MusicaPygame(SonidoPygame):

    def __init__(self, media, ruta):
        SonidoPygame.__init__(self, media, ruta)


class Motor(object):
    """Representa la ventana principal de pilas.

    Esta clase construirá el objeto apuntado por el atributo
    ``pilas.motor``, asi que será el representante de todas
    las funcionalidades multimedia.

    Internamente, este motor, tratará de usar OpenGl para acelerar
    el dibujado en pantalla si la tarjeta de video lo soporta.
    """

    def __init__(self, usar_motor, permitir_depuracion, audio):
        import sys

        if not '-i' in sys.argv:
            self._iniciar_aplicacion()

        self.usar_motor = usar_motor

        self.nombre = usar_motor
        self.permitir_depuracion = permitir_depuracion

        self._inicializar_variables()
        self._inicializar_sistema_de_audio(audio)

        # Creamos la variable para controlar la ventana de log
        self._widgetlog = None

    def _iniciar_aplicacion(self):
        self.app = QtGui.QApplication([])
        self.app.setApplicationName("pilas")

    def _inicializar_variables(self):
        self.camara_x = 0
        self.camara_y = 0
        self.libreria_imagenes = LibreriaImagenes()

    def _inicializar_sistema_de_audio(self, audio):
        sistemas_de_sonido = ['deshabilitado', 'pygame', 'phonon', 'gst']

        if audio not in sistemas_de_sonido:
            error = "El sistema de audio '%s' es invalido" % (audio)
            sugerencia = ". Use alguno de los siguientes: %s" % (str(sistemas_de_sonido))
            raise Exception(error + sugerencia)

        if audio == 'gst':
            try:
                import gst
            except ImportError:
                raise Exception("Error, el sistema de audio GST (gstreamer) no esta disponible.")
        elif audio == 'phonon':
            from PyQt4 import phonon
            self.media = phonon.Phonon.MediaObject()
            self.audio = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory)
            self.path = phonon.Phonon.createPath(self.media, self.audio)
            self.player = self.media
            self.clase_sonido = SonidoPhonon
            self.clase_musica = MusicaPhonon
        elif audio == 'pygame':
            try:
                import pygame
                pygame.mixer.init()
                self.player = None
                self.clase_sonido = SonidoPygame
                self.clase_musica = MusicaPygame
            except ImportError:
                raise Exception("Error, el sistema de audio pygame no esta disponible")
                audio = "deshabilitado"
        elif audio == 'gst':
            self.player = gst.element_factory_make("playbin2", "player")
            self.clase_sonido = SonidoGST
            self.clase_musica = MusicaGST

        # Si se deshabilita el sistema de sonido completo.
        if audio == 'deshabilitado':
            self.player = None
            self.clase_sonido = SonidoDeshabilitado
            self.clase_musica = MusicaDeshabilitada

    def terminar(self):
        self.ventana.close()

    def iniciar_ventana(self, ancho, alto, titulo, pantalla_completa,
                        gestor_escenas, rendimiento, centrado):
        self.ventana = Ventana()
        self.ventana.resize(ancho, alto)

        if centrado:
            resolucion_pantalla = QtGui.QDesktopWidget().screenGeometry()
            self.ventana.move((resolucion_pantalla.width() - ancho)/2, (resolucion_pantalla.height() - alto)/2)

        mostrar_ventana = True

        if self.usar_motor == 'qtgl':
            self.canvas = CanvasOpenGlWidget(self, ancho, alto, gestor_escenas,
                                             self.permitir_depuracion, rendimiento)
        else:
            self.canvas = CanvasNormalWidget(self, ancho, alto, gestor_escenas,
                                             self.permitir_depuracion, rendimiento)

        self.ventana.set_canvas(self.canvas)
        self.canvas.setFocus()

        self.ancho_original = ancho
        self.alto_original = alto
        self.titulo = titulo
        self.ventana.setWindowTitle(self.titulo)

        if mostrar_ventana:
            self.ventana.show()
            self.ventana.raise_()

        if pantalla_completa:
            self.canvas.pantalla_completa()

    def modificar_ventana(self, ancho, alto, titulo, pantalla_completa):
        self.titulo = titulo
        self.ventana.setWindowTitle(self.titulo)
        self.canvas.original_width = ancho
        self.canvas.original_height = alto
        self.ventana.resize(ancho, alto)

        if pantalla_completa:
            self.canvas.pantalla_completa()
        else:
            self.canvas.pantalla_modo_ventana()

    def ocultar_puntero_del_mouse(self):
        self.canvas.setCursor(QtGui.QCursor(Qt.BlankCursor))

    def mostrar_puntero_del_mouse(self):
        self.canvas.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def ejecutar_bucle_principal(self):
        if getattr(self, 'app', None):
            sys.exit(self.app.exec_())

    def definir_centro_de_la_camara(self, x, y):
        self.camara_x = x
        self.camara_y = y

    def obtener_centro_de_la_camara(self):
        return (self.camara_x, self.camara_y)

    def centro_fisico(self):
        "Centro de la ventana para situar el punto (0, 0)"
        return self.ancho_original/2, self.alto_original/2

    @dev.deprecated(se_desactiva_en="0.80", se_elimina_en="0.81",
                    reemplazo="pilas.mundo.obtener_area")
    def obtener_area(self):
        return (self.ancho_original, self.alto_original)

    def obtener_area_de_texto(self, cadena, magnitud=10, vertical=False, fuente=None, ancho=0):
        pic = QtGui.QPicture()
        p = QtGui.QPainter(pic)

        if fuente:
            nombre_de_fuente = Texto.cargar_fuente_desde_cache(fuente)
        else:
            nombre_de_fuente = p.font().family()

        font = QtGui.QFont(nombre_de_fuente, magnitud)
        p.setFont(font)

        alto = 0

        if vertical:
            lineas = [t for t in cadena]
        else:
            lineas = cadena.split('\n')

        if not ancho:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        else:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop

        for line in lineas:
            if line == '':
                line = ' '

            brect = p.drawText(QtCore.QRect(0, 0, ancho, 2000), flags, line)
            ancho = max(ancho, brect.width())
            alto += brect.height()

        p.end()
        return (ancho, alto)

    def obtener_actor(self, imagen, x, y):
        return Actor(imagen, x, y)

    def obtener_texto(self, texto, magnitud, vertical=False, fuente=None, color=pilas.colores.negro, ancho=None):
        return Texto(texto, magnitud, self, vertical, fuente, color=color, ancho=ancho)

    def obtener_grilla(self, ruta, columnas, filas):
        return Grilla(ruta, columnas, filas)

    def cargar_sonido(self, ruta):
        return self.clase_sonido(self.player, ruta)

    def cargar_musica(self, ruta):
        return self.clase_musica(self.player, ruta)

    def deshabilitar_sonido(self, estado=True):
        self.clase_sonido.deshabilitado = estado

    def deshabilitar_musica(self, estado=True):
        self.clase_musica.deshabilitado = estado

    def cargar_imagen(self, ruta):
        #if pilas.mundo.motor.libreria_imagenes.tiene(ruta):
        #    return pilas.mundo.motor.libreria_imagenes.obtener_imagen(ruta)
        #else:
        #  return Imagen(ruta)
        return Imagen(ruta)

    def obtener_lienzo(self):
        return Lienzo()

    def obtener_superficie(self, ancho, alto):
        return Superficie(ancho, alto)

    def log(self, params):
        if (self._widgetlog == None):
            self._widgetlog = WidgetLog()
        else:
            self._widgetlog.show()

        self._widgetlog.imprimir(params)

    def capturar_pantalla(self, nombre_archivo):
        self.canvas.save_to_disk(nombre_archivo)
