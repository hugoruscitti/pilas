# -*- coding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PyQt4 import QtCore, QtGui, phonon
from PyQt4.QtCore import Qt
from PyQt4.QtOpenGL import QGLWidget
from pilas import actores, colores, depurador, eventos, fps
from pilas import imagenes, simbolos, utils
import copy
import os
import pilas
import sys
import traceback


class Ventana(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setStyleSheet("QWidget {background-color : #222}")

    def set_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.setParent(self)

    def resizeEvent(self, event):
        self.canvas.resize_to(self.width(), self.height())


class CanvasWidget(QGLWidget):

    def __init__(self, motor, lista_actores, ancho, alto, gestor_escenas, permitir_depuracion):
        QGLWidget.__init__(self, None)
        self.painter = QtGui.QPainter()
        self.setMouseTracking(True)

        self.pausa_habilitada = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.motor = motor
        self.lista_actores = lista_actores
        self.fps = fps.FPS(60, True)

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

        self.painter.fillRect(0, 0, self.original_width, self.original_height, QtGui.QColor(128, 128, 128))
        self.depurador.comienza_dibujado(self.motor, self.painter)

        actores_a_eliminar = []

        if self.gestor_escenas.escena_actual():
            actores_de_la_escena = self.gestor_escenas.escena_actual().actores
            for actor in actores_de_la_escena:
                #if actor._vivo:
                try:
                    if not actor.esta_fuera_de_la_pantalla():
                        actor.dibujar(self.painter)
                except Exception:
                    print traceback.format_exc()
                    print sys.exc_info()[0]
                    actor.eliminar()

                self.depurador.dibuja_al_actor(self.motor, self.painter, actor)
                #else:
                #    actores_a_eliminar.append(actor)

                #for x in actores_a_eliminar:
                #    actores_de_la_escena.remove(x)

        self.depurador.termina_dibujado(self.motor, self.painter)
        self.painter.end()

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
        dx, dy = x - self.mouse_x, y - self.mouse_y

        izquierda, derecha, arriba, abajo = utils.obtener_bordes()
        x = max(min(derecha, x), izquierda)
        y = max(min(arriba, y), abajo)

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

        self.gestor_escenas.escena_actual().click_de_mouse.emitir(x=x, y=y, dx=0, dy=0)

    def mouseReleaseEvent(self, e):
        escala = self.escala
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x()/escala, e.pos().y()/escala)

        self.gestor_escenas.escena_actual().termina_click.emitir(x=x, y=y, dx=0, dy=0)

    def _obtener_codigo_de_tecla_normalizado(self, tecla_qt):
        teclas = {
            QtCore.Qt.Key_Left: simbolos.IZQUIERDA,
            QtCore.Qt.Key_Right: simbolos.DERECHA,
            QtCore.Qt.Key_Up: simbolos.ARRIBA,
            QtCore.Qt.Key_Down: simbolos.ABAJO,
            QtCore.Qt.Key_Space: simbolos.SELECCION,
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

class CanvasWidgetSugar(CanvasWidget):

    def _iniciar_aplicacion(self):
        self.app = None

    def ejecutar_bucle_principal(self, mundo, ignorar_errores):
        pass

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

        if ruta.lower().endswith("jpeg") or ruta.lower().endswith("jpg"):
            try:
                self._imagen = self.cargar_jpeg(ruta)
            except:
                self._imagen = QtGui.QPixmap(ruta)
        else:
            self._imagen = QtGui.QPixmap(ruta)

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
        return "<Imagen del archivo '%s'>" %(nombre_imagen)


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
        ha_reiniciado = False
        cuadro_actual = self._cuadro + 1

        if cuadro_actual >= self.cantidad_de_cuadros:
            cuadro_actual = 0
            ha_reiniciado = True

        self.definir_cuadro(cuadro_actual)
        return ha_reiniciado

    def obtener_cuadro(self):
        return self._cuadro

    def dibujarse_sobre_una_pizarra(self, pizarra, x, y):
        pizarra.pintar_parte_de_imagen(self, self.dx, self.dy, self.cuadro_ancho, self.cuadro_alto, x, y)


class Texto(Imagen):

    def __init__(self, texto, magnitud, motor, vertical=False):
        self.vertical = vertical
        self._ancho, self._alto = motor.obtener_area_de_texto(texto, magnitud, vertical)

    def _dibujar_pixmap(self, painter, dx, dy):
        nombre_de_fuente = painter.font().family()
        fuente = QtGui.QFont(nombre_de_fuente, self.magnitud)
        metrica = QtGui.QFontMetrics(fuente)

        r, g, b, a = self.color.obtener_componentes()
        painter.setPen(QtGui.QColor(r, g, b))
        painter.setFont(fuente)

        if self.vertical:
            lines = [t for t in self.texto]
        else:
            lines = self.texto.split('\n')

        for line in lines:
            painter.drawText(dx, dy + self._alto, line)
            dy += metrica.height()

    def ancho(self):
        return self._ancho

    def alto(self):
        return self._alto


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

        if not fuente:
            fuente = painter.font().family()

        painter.setFont(QtGui.QFont(fuente, magnitud))
        painter.drawText(x, y, cadena)

    def pintar(self, painter, color):
        r, g, b, a = color.obtener_componentes()
        ancho, alto = pilas.mundo.motor.obtener_area()
        painter.fillRect(0, 0, ancho, alto, QtGui.QColor(r, g, b))

    def linea(self, painter, x0, y0, x1, y1, color=colores.negro, grosor=1):
        x0, y0 = utils.hacer_coordenada_pantalla_absoluta(x0, y0)
        x1, y1 = utils.hacer_coordenada_pantalla_absoluta(x1, y1)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        painter.setPen(pen)
        painter.drawLine(x0, y0, x1, y1)

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
        painter.drawEllipse(x -radio, y-radio, radio*2, radio*2)

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

    def pintar(self, color):
        r, g, b, a = color.obtener_componentes()
        self._imagen.fill(QtGui.QColor(r, g, b, a))

    def pintar_parte_de_imagen(self, imagen, origen_x, origen_y, ancho, alto, x, y):
        self.canvas.begin(self._imagen)
        self.canvas.drawPixmap(x, y, imagen._imagen, origen_x, origen_y, ancho, alto)
        self.canvas.end()

    def pintar_imagen(self, imagen, x=0, y=0):
        self.pintar_parte_de_imagen(imagen, 0, 0, imagen.ancho(), imagen.alto(), x, y)

    def texto(self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro):
        self.canvas.begin(self._imagen)
        r, g, b, a = color.obtener_componentes()
        self.canvas.setPen(QtGui.QColor(r, g, b))
        dx = x
        dy = y

        if not fuente:
            fuente = self.canvas.font().family()

        font = QtGui.QFont(fuente, magnitud)
        self.canvas.setFont(font)
        metrica = QtGui.QFontMetrics(font)

        for line in cadena.split('\n'):
            self.canvas.drawText(dx, dy, line)
            dy += metrica.height()

        self.canvas.end()

    def circulo(self, x, y, radio, color=colores.negro, relleno=False, grosor=1):
        self.canvas.begin(self._imagen)

        r, g, b, a = color.obtener_componentes()
        color = QtGui.QColor(r, g, b)
        pen = QtGui.QPen(color, grosor)
        self.canvas.setPen(pen)

        if relleno:
            self.canvas.setBrush(color)

        self.canvas.drawEllipse(x -radio, y-radio, radio*2, radio*2)
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


class Actor(BaseActor):

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):

        if isinstance(imagen, str):
            self.imagen = imagenes.cargar(imagen)
        else:
            self.imagen = imagen

        self.x = x
        self.y = y
        BaseActor.__init__(self)

    def definir_imagen(self, imagen):
        # permite que varios actores usen la misma grilla.
        if isinstance(imagen, Grilla):
            self.imagen = copy.copy(imagen)
        else:
            self.imagen = imagen

    def obtener_imagen(self):
        return self.imagen

    def dibujar(self, painter):
        escala_x, escala_y = self._escala_x, self._escala_y

        if self._espejado:
            escala_x *= -1

        if not self.fijo:
            x = self.x - pilas.mundo.motor.camara_x
            y = self.y - pilas.mundo.motor.camara_y
        else:
            x = self.x
            y = self.y

        self.imagen.dibujar(painter, x, y, self.centro_x, self.centro_y,
                escala_x, escala_y, self._rotacion, self._transparencia)


class Sonido:
    deshabilitado = False

    def __init__(self, media, ruta):
        self.media = media
        self.ruta = ruta

        self.source = phonon.Phonon.MediaSource(ruta)
        self.sonido = phonon.Phonon.createPlayer(phonon.Phonon.GameCategory, self.source)

    def reproducir(self):
        if not self.deshabilitado:
            self.sonido.seek(0)
            self.sonido.play()

    def detener(self):
        self.sonido.stop()


class Musica(Sonido):

    def __init__(self, media, ruta):
        Sonido.__init__(self, media, ruta)


class Motor(object):
    """Representa la ventana principal de pilas.

    Esta clase construirá el objeto apuntado por el atributo
    ``pilas.motor``, asi que será el representante de todas
    las funcionalidades multimedia.

    Internamente, este motor, tratará de usar OpenGl para acelerar
    el dibujado en pantalla si la tarjeta de video lo soporta.
    """

    def __init__(self, usar_motor, permitir_depuracion):
        if usar_motor not in ['qtwidget', 'qtsugar']:
            self._iniciar_aplicacion()

        self.usar_motor = usar_motor

        self.nombre = usar_motor
        self.permitir_depuracion = permitir_depuracion

        self._inicializar_variables()
        self._inicializar_sistema_de_audio()

    def _iniciar_aplicacion(self):
        self.app = QtGui.QApplication([])
        self.app.setApplicationName("pilas")

    def _inicializar_variables(self):
        self.camara_x = 0
        self.camara_y = 0

    def _inicializar_sistema_de_audio(self):
        self.media = phonon.Phonon.MediaObject()
        self.audio = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory)
        self.path = phonon.Phonon.createPath(self.media, self.audio)

    def terminar(self):
        self.ventana.close()

    def iniciar_ventana(self, ancho, alto, titulo, pantalla_completa, gestor_escenas):
        self.ventana = Ventana()
        self.ventana.resize(ancho, alto)

        if self.usar_motor in ['qtwidget', 'qtsugar']:
            mostrar_ventana = False
            self.canvas = CanvasWidgetSugar(self, actores.todos, ancho, alto, gestor_escenas, self.permitir_depuracion)
        else:
            mostrar_ventana = True
            self.canvas = CanvasWidget(self, actores.todos, ancho, alto, gestor_escenas, self.permitir_depuracion)

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

    def ejecutar_bucle_principal(self, mundo, ignorar_errores):
        sys.exit(self.app.exec_())

    def definir_centro_de_la_camara(self, x, y):
        self.camara_x = x
        self.camara_y = y

    def obtener_centro_de_la_camara(self):
        return (self.camara_x, self.camara_y)

    def centro_fisico(self):
        "Centro de la ventana para situar el punto (0, 0)"
        return self.ancho_original/2, self.alto_original/2

    def obtener_area(self):
        return (self.ancho_original, self.alto_original)

    def obtener_area_de_texto(self, texto, magnitud=10, vertical=False):
        ancho = 0
        alto = 0

        fuente = QtGui.QFont()
        fuente.setPointSize(magnitud)
        metrica = QtGui.QFontMetrics(fuente)

        if vertical:
            lineas = [t for t in texto]
        else:
            lineas = texto.split('\n')

        for linea in lineas:
            ancho = max(ancho, metrica.width(linea))
            alto += metrica.height()

        return ancho, alto

    def obtener_actor(self, imagen, x, y):
        return Actor(imagen, x, y)

    def obtener_texto(self, texto, magnitud, vertical=False):
        return Texto(texto, magnitud, self, vertical)

    def obtener_grilla(self, ruta, columnas, filas):
        return Grilla(ruta, columnas, filas)

    def cargar_sonido(self, ruta):
        return Sonido(self.media, ruta)

    def cargar_musica(self, ruta):
        return Musica(self.media, ruta)

    def deshabilitar_sonido(self, estado=True):
        Sonido.deshabilitado = estado

    def deshabilitar_musica(self, estado=True):
        Musica.deshabilitado = estado

    def cargar_imagen(self, ruta):
        return Imagen(ruta)

    def obtener_lienzo(self):
        return Lienzo()

    def obtener_superficie(self, ancho, alto):
        return Superficie(ancho, alto)
