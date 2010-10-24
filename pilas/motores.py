# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pygame
from PySFML import sf
from pilas.simbolos import *
import eventos
import pilas


class Sonido:

    def __init__(self, buffer):
        self.buffer = buffer
        self.sonido = sf.Sound(buffer)
        pass

    def reproducir(self):
        self.sonido.Play()
    
    def Play(self):
        self.reproducir()


class Pygame:
    """Representa la capa de interaccion con la biblioteca Pygame.

    Esto permite que tus juegos realizados con pilas funcionen
    en cualquier equipo que tenga instalada la biblioteca pygame,
    por ejemplo equipos como OLPC o simplemente aquellos que no
    tengan aceleradoras de graficos OpenGL."""

    class Sprite:

        def __init__(self, *k, **kv):
            print "Iniciando la capa de sprite..."
            pass

    SpriteActor = Sprite

    def __init__(self):
        import pilas.colores
        pygame.init()
        pilas.colores.gris = (200, 200, 200)

    def crear_ventana(self, ancho, alto, titulo):
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(titulo)
        return self.ventana


    def centrar_ventana(self):
        pass


    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        mapa = {
                IZQUIERDA: pygame.K_LEFT,
                DERECHA: pygame.K_RIGHT,
                ARRIBA: pygame.K_UP,
                ABAJO: pygame.K_DOWN,
                BOTON: pygame.K_SPACE,
                }

        return pygame.key.get_pressed()[mapa[tecla]]

    def procesar_y_emitir_eventos(self):
        "Procesa todos los eventos que la biblioteca pygame pone en una cola."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                #self.procesar_evento_teclado(event)
                if event.key == pygame.K_q:
                    import sys
                    sys.exit(0)
            elif event.type == pygame.MOUSEMOTION:
                # Notifica el movimiento del mouse con una señal
                x, y = event.pos
                dx, dy = event.rel
                eventos.mueve_mouse.send("ejecutar", x=x, y=-y, dx=dx, dy=dy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if event.button == 3:
                    eventos.mueve_rueda.send("ejecutar", delta=1)
                    print "HAAAAA, no se de donde sacar el delta de movimiento de la rueda!!!"
                else:
                    eventos.click_de_mouse.send("ejecutar", button=event.button, x=x, y=-y)

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                eventos.termina_click.send("ejecutar", button=event.button, x=x, y=-y)


    def actualizar_pantalla(self):
        pygame.display.flip()

    def pintar(self, color):
        self.ventana.fill(color)

    def cargar_imagen(self, ruta):
        # TODO: Optimizar la imagen preservando el canal alpha.
        return pygame.image.load(ruta)

class pySFML:

    class Sprite:

        def __init__(self, *k, **kv):
            print "Iniciando la capa de sprite..."
            pass

    SpriteActor = Sprite

    def __init__(self):
        import pilas.colores
        # Se usan para calcular el dx y dy del movimiento
        # del mouse porque pySFML no lo reporta de forma relativa.
        self.mouse_x = 0
        self.mouse_y = 0
        pilas.colores.gris = sf.Color(200, 200, 200)

    def crear_ventana(self, ancho, alto, titulo):
        ventana = sf.RenderWindow(sf.VideoMode(ancho, alto), titulo)
        # Define que la coordenada (0, 0) sea el centro de la ventana.
        view = ventana.GetDefaultView()
        view.SetCenter(0, 0)
        self.input = ventana.GetInput()
        self.event = sf.Event()
        self.vista_de_camara = ventana.GetDefaultView()
        self.ventana = ventana
        return ventana

    def pulsa_tecla(self, tecla):
        "Indica si una tecla esta siendo pulsada en este instante."

        mapa = {
                IZQUIERDA: sf.Key.Left,
                DERECHA: sf.Key.Right,
                ARRIBA: sf.Key.Up,
                ABAJO: sf.Key.Down,
                BOTON: sf.Key.Space,
                }

        return self.input.IsKeyDown(mapa[tecla])


    def centrar_ventana(self):
        "Coloca la ventana principal en el centro del escritorio."

        vm = sf.VideoMode(100, 100)

        # Obtiene la resolución del escritorio y la ventana.
        desktop_mode = vm.GetDesktopMode()
        w, h = self.ventana.GetWidth(), self.ventana.GetHeight()

        # Calcula cual debería la coordenada para centrar la ventana.
        to_x = desktop_mode.Width/2 - w/2
        to_y = desktop_mode.Height/2 - h/2

        self.ventana.SetPosition(to_x, to_y)

    def procesar_y_emitir_eventos(self):
        "Procesa todos los eventos que la biblioteca SFML pone en una cola."
        event = self.event

        while self.ventana.GetEvent(self.event):
            if event.Type == sf.Event.KeyPressed:
                #self.procesar_evento_teclado(event)

                if event.Key.Code == sf.Key.Q:
                    import sys
                    sys.exit(0)
                    #self.mundo.terminar()

            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal

                x, y = event.MouseMove.X, event.MouseMove.Y

                if x > 0 and y > 0:
                    x, y = self.ventana.ConvertCoords(x, y)

                    dx = x - self.mouse_x
                    dy = self.mouse_y - y
                    self.mouse_x = x
                    self.mouse_y = y

                    eventos.mueve_mouse.send("ejecutar", x=x, y=-y, dx=dx, dy=dy)

            elif event.Type == sf.Event.MouseButtonPressed:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonReleased:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseMove.Y)
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)

    def actualizar_pantalla(self):
        self.ventana.Display()

    def definir_centro_de_la_camara(self, x, y):
        view = self.ventana.GetDefaultView()
        view.SetCenter(x, y)

    def obtener_centro_de_la_camara(self):
        view = self.ventana.GetDefaultView()
        return view.GetCenter()

    def pintar(self, color):
        self.ventana.Clear(color)

            
    def cargar_sonido(self, ruta):
        buff = sf.SoundBuffer()
        buff.LoadFromFile(ruta)
        return Sonido(buff)

    def cargar_imagen(self, ruta):
        image = sf.Image()
        image.LoadFromFile(ruta)
        return image
