# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import sys
from PyQt4 import QtGui, QtCore

import motor
from pilas import imagenes
from pilas import actores
from pilas import eventos
from pilas import utils

from pilas import fps
from pilas import simbolos


class BaseActor:
    
    def __init__(self):
        self._rotacion = 0
        self._escala = 1
        self.centro_x = 0
        self.centro_y = 0

    def obtener_ancho(self):
        return self.imagen.ancho()

    def obtener_alto(self):
        return self.imagen.alto()

    def obtener_area(self):
        return self.obtener_ancho(), self.obtener_alto()

    def definir_centro(self, x, y):
        self.centro_x = x
        self.centro_y = y

    def obtener_posicion(self):
        return self.x, self.y

    def definir_posicion(self, x, y):
        self.x, self.y = x, y

    def obtener_escala(self):
        return self._escala

    def definir_escala(self, s):
        self._escala = s

    def definir_transparencia(self, nuevo_valor):
        pass

    def obtener_rotacion(self):
        return self._rotacion

    def definir_rotacion(self, r):
        self._rotacion = r
        
    def set_espejado(self, espejado):        
        pass
        
class QtImagen():

    def __init__(self, ruta):
        self._imagen = QtGui.QPixmap(ruta)
        print self._imagen

    def ancho(self):
        return self._imagen.size().width()

    def alto(self):
        return self._imagen.size().height()

    def centro(self):
        "Retorna una tupla con la coordenada del punto medio del la imagen."
        return (self.ancho()/2, self.alto()/2)

    def dibujar(self, motor, x, y, dx=0, dy=0, escala_x=1, escala_y=1, rotacion=0):
        """Dibuja la imagen sobre la ventana que muestra el motor.

           x, y: indican la posicion dentro del mundo.
           dx, dy: es el punto centro de la imagen (importante para rotaciones).
           escala_x, escala_yindican cambio de tamano (1 significa normal).
           rotacion: angulo de inclinacion en sentido de las agujas del reloj.
        """

        motor.canvas.save()
        motor.canvas.translate(x + 320, 240 - y)
        motor.canvas.rotate(rotacion)
        motor.canvas.scale(escala_x, escala_y)
        motor.canvas.drawPixmap(-dx, -dy, self._imagen)
        motor.canvas.restore()

        
class QtActor(BaseActor):

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):

        if isinstance(imagen, str):
            self.imagen = imagenes.cargar(imagen)
        else:
            self.imagen = imagen

        self.x = x
        self.y = y
        BaseActor.__init__(self)

    def definir_imagen(self, imagen):
        self.imagen = imagen

    def obtener_imagen(self):
        return self.imagen

    def dibujar(self, motor):
        motor.canvas.save()
        # TODO: usando 320 x 240 para representar el centro de la ventana.
        x, y = utils.convertir_de_posicion_relativa_a_fisica(self.x, self.y)
        motor.canvas.translate(self.x + 320, 240 - self.y)
        motor.canvas.rotate(self._rotacion)
        motor.canvas.scale(self._escala, self._escala)
        motor.canvas.drawPixmap(-self.centro_x, -self.centro_y, self.imagen)
        motor.canvas.restore()


class SFMLTexto(BaseActor):
    # TODO


    def __init__(self, texto="None", x=0, y=0):
        sf.String.__init__(self, texto)
        BaseActor.__init__(self)
        self.color = pilas.colores.negro

    def obtener_texto(self):
        return self.GetText()

    def definir_texto(self, text):
        self.SetText(text)
        self._definir_eje_en_el_centro()

    def obtener_magnitud(self):
        return self.GetSize()

    def definir_magnitud(self, size):
        self.SetSize(size)
        self._definir_eje_en_el_centro()

    def _definir_eje_en_el_centro(self):
        rect = self.GetRect()
        size = (rect.GetWidth(), rect.GetHeight())
        self.SetCenter(size[0]/2, size[1]/2)

    def obtener_color(self):
        return self.GetColor()

    def definir_color(self, k):
        self.SetColor(sf.Color(*k.obtener_componentes()))

    def dibujar(self, aplicacion):
        aplicacion.Draw(self)
        
    def colisiona_con_un_punto(self, x, y):
        return False

    def obtener_ancho(self):
        rect = self.GetRect()
        return rect.GetWidth()

    def obtener_alto(self):
        rect = self.GetRect()
        return rect.GetHeight()

class QtSonido:

    def __init__(self, ruta):
        self._sonido = QtGui.QSound(ruta)

    def reproducir(self):
        self._sonido.play()
        
    def definir_pitch(self, pitch):
        pass
        #self.sonido.SetPitch(pitch)

        
class SFMLCanvas:
    "Representa una superficie sobre la que se puede dibujar usando cairo."
    # TODO

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, ancho, alto)
        self.image = sf.Image()
        self.context = cairo.Context(self.surface)
        self.actualizar()

    def actualizar(self):
        self.image.LoadFromPixels(self.ancho, self.alto, self.surface.get_data())

    def limpiar(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.ancho, self.alto)
        self.context = cairo.Context(self.surface)       

class QtGrilla:

    def __init__(self, ruta, columnas=1, filas=1):
        self.image = imagenes.cargar(ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = self.image.size().width() / columnas
        self.cuadro_alto = self.image.size().height() / filas

    def dibujar(self, motor, cuadro):
        motor.canvas.save()
        # TODO: usando 320 x 240 para representar el centro de la ventana.
        x, y = utils.convertir_de_posicion_relativa_a_fisica(self.x, self.y)
        motor.canvas.translate(self.x + 320, 240 - self.y)
        motor.canvas.rotate(self._rotacion)
        motor.canvas.scale(self._escala, self._escala)
        motor.canvas.drawPixmap(-self.centro_x, -self.centro_y, self.imagen)
        motor.canvas.restore()


    def definir_cuadro(self, cuadro):
        self.cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        dx = frame_col * self.cuadro_ancho - self.sub_rect.Left
        dy = frame_row * self.cuadro_alto - self.sub_rect.Top

        self.sub_rect.Offset(dx, dy)

    def avanzar(self):
        ha_reiniciado = False
        cuadro_actual = self.cuadro + 1

        if cuadro_actual >= self.cantidad_de_cuadros:
            cuadro_actual = 0
            ha_reiniciado = True

        self.definir_cuadro(cuadro_actual)
        return ha_reiniciado

    def obtener_cuadro(self):
        return self.cuadro

    def obtener_dx(self):
        frame_col = self.cuadro % self.columnas
        dx = frame_col * self.cuadro_ancho
        return dx

    def obtener_dy(self):
        frame_row = self.cuadro / self.columnas
        dy = frame_row * self.cuadro_alto
        return dy
               
class aaaaaaaaaaaaaaaaaaaaVentana(QtGui.QWidget):

    def __init__(self, ancho, alto, titulo):
        super(Ventana, self).__init__()
        self.init()
        self.sprites = []

        '''
        self.mouse = QtGui.QCursor()

        time = QtCore.QTimer()
        time.singleShot(50, self.hacer_flotante_la_ventana_en_i3)
        '''

    def do_update(self):
        self.update()
        '''
        position = self.mapFromGlobal(QtGui.QCursor.pos())
        x = position.x()
        y = position.y()
        self.sprites[0].x = x
        self.sprites[0].y = y
        '''

    def hacer_flotante_la_ventana_en_i3(self):
        try:
            subprocess.call(['i3-msg', 't'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            pass

    def paintEvent(self, event):
        self.canvas.begin(self)
        #self.qp.scale(self.scale_x, self.scale_y)
        self.canvas.setClipRect(0, 0, 640, 480)

        # Hace que el centro de coordenadas sea (0, 0)
        # self.qp.setWindow(-320, -240, 640, 480)
        # self.qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.render(event, self.canvas)
        self.canvas.end()




    def mouseReleaseEvent(self, event):
        print "Han soltado el boton:", event.button()

    def keyPressEvent(self, event):
        print "Pulsa la tecla:", event.key()

    def wheelEvent(self, event):
        print "Mueve rueda:", event.delta()

    def timerEvent(self, event):
        self.do_update()

    def render(self, event, qp):
        for r in self.sprites:
            r.dibujar(self.canvas)

        
class Qt(motor.Motor, QtGui.QWidget):

    app = QtGui.QApplication([])

    def __init__(self):
        QtGui.QWidget.__init__(self)
        motor.Motor.__init__(self)
        self.canvas = QtGui.QPainter()
        self.setMouseTracking(True)
        self.fps = fps.FPS(60, True)
        self.pausa_habilitada = False

    def obtener_actor(self, imagen, x, y):
        return QtActor(imagen, x, y)

    def obtener_texto(self, texto, x, y):
        return SFMLTexto(texto, x, y)

    def obtener_posicion_del_mouse(self):
        #return (self.mouse_x, self.mouse_y)
        pass
    
    def obtener_canvas(self, ancho, alto):
        return SFMLCanvas(ancho, alto)
    
    def obtener_grilla(self, ruta, columnas, filas):
        return QtGrilla(ruta, columnas, filas)

    def iniciar_ventana(self, ancho, alto, titulo):
        self.ancho = ancho
        self.alto = alto
        self.titulo = titulo
        self.setGeometry(100, 100, self.ancho, self.alto)
        self.setWindowTitle(self.titulo)
        self.show()
        self.setFixedSize(self.ancho, self.alto)
        self.startTimer(1000/100.0)

    def ocultar_puntero_del_mouse(self):
        self.ventana.ShowMouseCursor(False)

    def mostrar_puntero_del_mouse(self):
        self.ventana.ShowMouseCursor(True)

    def cerrar_ventana(self):
        self.ventana.Close()

    def dibujar_circulo(self, x, y, radio, color, color_borde):
        delta = radio / 2
        circulo = sf.Shape.Circle(0, 0, delta, 
                sf.Color(*color.obtener_componentes()), 2, 
                sf.Color(*color_borde.obtener_componentes()))
        circulo.SetCenter(0, 0)
        circulo.SetPosition(x, -y)
        self.ventana.Draw(circulo)

    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        '''
        mapa = {
                IZQUIERDA: sf.Key.Left,
                DERECHA: sf.Key.Right,
                ARRIBA: sf.Key.Up,
                ABAJO: sf.Key.Down,
                BOTON: sf.Key.Space,
                SELECCION: sf.Key.Return,
                }

        return self.input.IsKeyDown(mapa[tecla])
        '''
        return False


    def centrar_ventana(self):
        "Coloca la ventana principal en el centro del escritorio."
        pass


    def procesar_y_emitir_eventos(self):
        "Procesa todos los eventos que la biblioteca SFML pone en una cola."
        return
        '''
        pass
        event = self.event

        while self.ventana.GetEvent(self.event):
            if event.Type == sf.Event.Closed:
                pilas.mundo.terminar()
            if event.Type == sf.Event.KeyPressed:
                self.procesar_evento_teclado(event)

                if event.Key.Code == sf.Key.Q and event.Key.Alt:
                    pilas.mundo.terminar()
            elif event.Type == sf.Event.TextEntered:

                eventos.pulsa_tecla.send("ejecutar", codigo=unichr(event.Text.Unicode)) 
            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal

                x, y = event.MouseMove.X, event.MouseMove.Y

                if x > 0 and y > 0:
                    x, y = self.ventana.ConvertCoords(x, y)
                    y = -y

                    # Se asegura de los eventos de mouse esten siempre
                    # dentro de la ventana.
                    x = min(320, x)
                    y = max(y, -240)

                    dx = x - self.mouse_x
                    dy = y - self.mouse_y

                    self.mouse_x = x
                    self.mouse_y = y

                    eventos.mueve_mouse.send("ejecutar", x=x, y=y, dx=dx, dy=dy)

            elif event.Type == sf.Event.MouseButtonPressed:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonReleased:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)
        '''

    def procesar_evento_teclado(self, event):
        code = event.Key.Code
        
        if code == sf.Key.P and event.Key.Alt:
            pilas.mundo.alternar_pausa()
        elif code == sf.Key.F4:
            pilas.motor.guardar_captura()
        elif code == sf.Key.F6:
            pilas.utils.listar_actores_en_consola()                
        elif code == sf.Key.F7:
            eventos.imprimir_todos()
        elif code in [sf.Key.F8, sf.Key.F9, sf.Key.F10, sf.Key.F11, sf.Key.F12]:
            pilas.mundo.depurador.pulsa_tecla(code)
        elif code == sf.Key.Escape:
            eventos.pulsa_tecla_escape.send("ejecutar")

    def actualizar_pantalla(self):
        self.ventana.update()

    def definir_centro_de_la_camara(self, x, y):
        view = self.ventana.GetDefaultView()
        view.SetCenter(x, y)

    def obtener_centro_de_la_camara(self):
        view = self.ventana.GetDefaultView()
        return view.GetCenter()

    def pintar(self, color):
        pass
            
    def cargar_sonido(self, ruta):
        return QtSonido(ruta)

    def cargar_imagen(self, ruta):
        return QtImagen(ruta)

    def obtener_imagen_cairo(self, imagen):
        """Retorna una superficie de cairo representando a la imagen.

        Esta funcion es util para pintar imagenes sobre una pizarra
        o el escenario de un videojuego.
        """
        import array

        pixels = array.array("B", imagen.GetPixels())

        w = imagen.GetWidth()
        h = imagen.GetHeight()

        return cairo.ImageSurface.create_for_data(pixels, cairo.FORMAT_RGB24, w, h)

    def guardar_captura(self):
        imagen = self.ventana.Capture()
        numero = self._obtener_numeracion_siguiente_imagen()
        nombre = "imagen_%d.png" %(numero)
        imagen.SaveToFile(nombre)
        print "Guardando el archivo %s" %(nombre)

    def _obtener_numeracion_siguiente_imagen(self):
        "Obtiene un numero de imagen para guardar una captura."
        lista_de_archivos = glob.glob("imagen_*.png")

        if lista_de_archivos:
            archivos = "\n".join(lista_de_archivos)
            patron = "_(.+).png"
            numeros = [int(x) for x in re.findall(patron, archivos)]
            numeros.sort()
            ultimo_numero = numeros[-1] + 1
        else:
            ultimo_numero = 1

        return ultimo_numero

    def ejecutar_bucle_principal(self, mundo, ignorar_errores):
        sys.exit(self.app.exec_())

        '''
        while not mundo.salir:

            # Invoca varias veces a la actualizacion si el equipo
            # es lento.
            for x in range(mundo.fps.actualizar()):
                # Mantiene el control de tiempo y lo reporta al sistema
                # de interpolaciones y tareas.

                self.procesar_y_emitir_eventos()
                
                if not mundo.pausa_habilitada:
                    mundo._realizar_actualizacion_logica(ignorar_errores)

            mundo.realizar_actualizacion_grafica()

        mundo.cerrar_ventana()
        '''

    def paintEvent(self, event):
        self.canvas.begin(self)

        #windowWidth = 640
        #windowHeight = (self.alto / self.ancho) * windowWidth;
        #alto = self.ancho * (480 / 640.0)
        #print alto

        #self.canvas.setViewport(0, 0, self.ancho, self.alto);
        #self.canvas.setWindow(0, 0, 640, 480)


        self.canvas.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, False)
        self.canvas.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.canvas.setRenderHint(QtGui.QPainter.Antialiasing, False)

        for actor in actores.todos:
            actor.dibujar(self)

        self.canvas.end()

    def timerEvent(self, event):
        self.realizar_actualizacion_logica()

        # Invoca el dibujado de la pantalla.
        self.update()

        '''
        self.procesar_y_emitir_eventos()
                
        if not self.mundo.pausa_habilitada:
            self.mundo._realizar_actualizacion_logica(self.ignorar_errores)

        self.mundo.realizar_actualizacion_grafica()
        '''

    def realizar_actualizacion_logica(self):
        for x in range(self.fps.actualizar()):
            if not self.pausa_habilitada:
                eventos.actualizar.send("Qt::timerEvent")

                for actor in actores.todos:
                    actor.actualizar()

    def resizeEvent(self, event):
        self.ancho = event.size().width()
        self.alto = event.size().height()

    def mousePressEvent(self, e):
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x(), e.pos().y())
        eventos.click_de_mouse.send("Qt::mousePressEvent", x=x, y=y, dx=0, dy=0)

    def mouseMoveEvent(self, e):
        x, y = utils.convertir_de_posicion_fisica_relativa(e.pos().x(), e.pos().y())
        eventos.mueve_mouse.send("Qt::mouseMoveEvent", x=x, y=y, dx=0, dy=0)

    def keyPressEvent(self, event):
        codigo_de_tecla = self.obtener_codigo_de_tecla_normalizado(event.key())
        eventos.pulsa_tecla.send("Qt::keyPressEvent", codigo=codigo_de_tecla, texto=event.text())

    def keyReleaseEvent(self, event):
        codigo_de_tecla = self.obtener_codigo_de_tecla_normalizado(event.key())
        eventos.suelta_tecla.send("Qt::keyReleaseEvent", codigo=codigo_de_tecla, texto=event.text())

    def obtener_codigo_de_tecla_normalizado(self, tecla_qt):
        teclas = {
            QtCore.Qt.Key_Left: simbolos.IZQUIERDA,
            QtCore.Qt.Key_Right: simbolos.DERECHA,
            QtCore.Qt.Key_Up: simbolos.ARRIBA,
            QtCore.Qt.Key_Down: simbolos.ABAJO,
            QtCore.Qt.Key_Space: simbolos.SELECCION,
            QtCore.Qt.Key_Return: simbolos.SELECCION,
        }

        if teclas.has_key(tecla_qt):
            return teclas[tecla_qt]
        else:
            return tecla_qt
