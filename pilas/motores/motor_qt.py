# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

#from PySFML import sf
from PyQt4 import QtGui, QtCore
from pilas.simbolos import *
import cairo
import pilas
from pilas import eventos
import motor
import glob
import sys
import re

ANCHO = 640
ALTO = 480

class BaseActor:
    
    def __init__(self):
        pass

    def obtener_ancho(self):
        pass

    def obtener_alto(self):
        pass

    def obtener_area(self):
        return self.obtener_ancho(), self.obtener_alto()

    def definir_centro(self, x, y):
        pass

    def obtener_posicion(self):
        pass

    def definir_posicion(self, x, y):
        pass

    def obtener_escala(self):
        pass

    def definir_escala(self, s):
        pass

    def definir_transparencia(self, nuevo_valor):
        pass

    def obtener_rotacion(self):
        pass

    def definir_rotacion(self, r):
        pass
        
    def set_espejado(self, espejado):        
        pass
        
        
class QtActor(BaseActor):

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):

        if isinstance(imagen, str):
            self.imagen = pilas.imagenes.cargar(imagen)
        else:
            self.imagen = imagen

        self.x = x
        self.y = y
        BaseActor.__init__(self)

    def definir_imagen(self, imagen):
        self.imagen = imagen

    def obtener_imagen(self):
        return self.imagen

    def dibujar(self, canvas):
        canvas.drawPixmap(self.x, self.y, self.imagen)


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

class SFMLSonido:
    # TODO

    def __init__(self, ruta):
        buff = sf.SoundBuffer()
        buff.LoadFromFile(ruta)
        self.buffer = buff
        self.sonido = sf.Sound(self.buffer)

    def reproducir(self):
        self.sonido.Play()
        
    def definir_pitch(self, pitch):
        self.sonido.SetPitch(pitch)
        
    def Play(self):
        self.reproducir()

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

class SFMLGrilla:
    # TODO

    def __init__(self, ruta, columnas=1, filas=1):
        self.image = pilas.imagenes.cargar(ruta)
        self.cantidad_de_cuadros = columnas * filas
        self.columnas = columnas
        self.filas = filas
        self.cuadro_ancho = self.image.GetWidth() / columnas
        self.cuadro_alto = self.image.GetHeight() / filas
        self.sub_rect = sf.IntRect(0, 0, self.cuadro_ancho, self.cuadro_alto)
        self.definir_cuadro(0)

    def definir_cuadro(self, cuadro):
        self.cuadro = cuadro

        frame_col = cuadro % self.columnas
        frame_row = cuadro / self.columnas

        dx = frame_col * self.cuadro_ancho - self.sub_rect.Left
        dy = frame_row * self.cuadro_alto - self.sub_rect.Top

        self.sub_rect.Offset(dx, dy)

    def asignar(self, sprite):
        "Define la imagen que tiene que tener el actor."

        sprite._actor.SetImage(self.image)
        sprite._actor.SetSubRect(self.sub_rect)

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
               
class Ventana(QtGui.QWidget):

    def __init__(self, ancho, alto, titulo):
        super(Ventana, self).__init__()
        self.init()
        self.canvas = QtGui.QPainter()
        self.sprites = []

        '''
        self.startTimer(1000/100.0)
        self.mouse = QtGui.QCursor()

        time = QtCore.QTimer()
        time.singleShot(50, self.hacer_flotante_la_ventana_en_i3)
        '''
        self.sprites.append(QtActor('aceituna.png'))

    def do_update(self):
        self.update()
        '''
        position = self.mapFromGlobal(QtGui.QCursor.pos())
        x = position.x()
        y = position.y()
        self.sprites[0].x = x
        self.sprites[0].y = y
        '''

    def init(self):
        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle('Prueba de concepto: Pilas sobre QT')
                                                                                                                 
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

    def resizeEvent(self, event):
        w, h = event.size().width(), event.size().height()
        self.scale_x = w / 640.0
        self.scale_y = h / 480.0

    def mousePressEvent(self, event):
        print "Han pulsado el boton:", event.button()

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

        
class Qt(motor.Motor):

    def __init__(self):
        motor.Motor.__init__(self)
        # Se usan para calcular el dx y dy del movimiento
        # del mouse porque pySFML no lo reporta de forma relativa.
        self.mouse_x = 0
        self.mouse_y = 0

    def obtener_actor(self, imagen, x, y):
        return SFMLActor(imagen, x, y)

    def obtener_texto(self, texto, x, y):
        return SFMLTexto(texto, x, y)

    def obtener_posicion_del_mouse(self):
        return (self.mouse_x, self.mouse_y)
    
    def obtener_canvas(self, ancho, alto):
        return SFMLCanvas(ancho, alto)
    
    def obtener_grilla(self, ruta, columnas, filas):
        return SFMLGrilla(ruta, columnas, filas)

    def crear_ventana(self, ancho, alto, titulo):
        self.app = QtGui.QApplication(sys.argv)

        ventana = Ventana(ancho, alto, titulo)
        ventana.show()
        self.ventana = ventana
        # Define que la coordenada (0, 0) sea el centro de la ventana.
        '''
        view = ventana.GetDefaultView()
        view.SetCenter(0, 0)
        self.input = ventana.GetInput()
        self.event = sf.Event()
        self.vista_de_camara = ventana.GetDefaultView()
        self.ventana = ventana
        return ventana
        '''
        return ventana

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
#self.ventana.Display()
        pass

    def definir_centro_de_la_camara(self, x, y):
        view = self.ventana.GetDefaultView()
        view.SetCenter(x, y)

    def obtener_centro_de_la_camara(self):
        view = self.ventana.GetDefaultView()
        return view.GetCenter()

    def pintar(self, color):
        pass
#self.ventana.Clear(sf.Color(*color.obtener_componentes()))
            
    def cargar_sonido(self, ruta):
        return SFMLSonido(ruta)

    def cargar_imagen(self, ruta):
        return QtGui.QPixmap(ruta)

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
