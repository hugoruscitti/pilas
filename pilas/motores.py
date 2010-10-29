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




class Pygame:
    """Representa la capa de interaccion con la biblioteca Pygame.

    Esto permite que tus juegos realizados con pilas funcionen
    en cualquier equipo que tenga instalada la biblioteca pygame,
    por ejemplo equipos como OLPC o simplemente aquellos que no
    tengan aceleradoras de graficos OpenGL."""

    import pilas.base

    class Sonido:

        def __init__(self, ruta):
            self.sonido = pygame.mixer.Sound(ruta)

        def reproducir(self):
            self.sonido.play()
        
        def Play(self):
            self.reproducir()

    class Actor(pilas.base.BaseActor, pygame.sprite.Sprite):
        """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

        Un objeto Actor se tiene que crear siempre indicando la imagen, ya
        sea como una ruta a un archivo como con un objeto Image. Por ejemplo::

            protagonista = Actor("protagonista_de_frente.png")

        es equivalente a:

            imagen = pilas.imagenes.cargar("protagonista_de_frente.png")
            protagonista = Actor(imagen)

        Luego, na vez que ha sido ejecutada la sentencia aparecerá en el centro de
        la pantalla el nuevo actor para que pueda manipularlo. Por ejemplo
        alterando sus propiedades::

            protagonista.x = 100
            protagonista.scale = 2
            protagonista.rotation = 30


        Estas propiedades tambien se pueden manipular mediante
        interpolaciones. Por ejemplo, para aumentar el tamaño del
        personaje de 1 a 5 en 7 segundos::

            protagonista.scale = pilas.interpolar(1, 5, 7)

        Si creas un sprite sin indicar la imagen se cargará
        una por defecto.
        """

        def __init__(self, image="sin_imagen.png"):

            if isinstance(image, str):
                image = pilas.imagenes.cargar(image)

            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            pilas.base.BaseActor.__init__(self) 
            self._escala_actual = 1
            
        def definir_imagen(self, imagen):
            self.image = imagen

        def dibujar(self, aplicacion):
            x, y = self.rect.topleft
            aplicacion.blit(self.image, (x + 320, y + 240))

        def duplicar(self, **kv):
            duplicado = self.__class__()

            for clave in kv:
                setattr(duplicado, clave, kv[clave])

            return duplicado

        def obtener_ancho(self):
            return self.rect.width

        def obtener_alto(self):
            return self.rect.height

        def __str__(self):
            return "<%s en (%d, %d)>" %(self.__class__.__name__, self.x, self.y)

        def obtener_area(self):
            return self.obtener_ancho(), self.obtener_alto()

        def definir_centro(self, x, y):
            print "No se puede cambiar el centro en pygame."

        def obtener_posicion(self):
            x, y = self.rect.center
            return x, -y

        def definir_posicion(self, x, y):
            self.rect.center = (x, -y)

        def obtener_escala(self):
            return self._escala_actual

        def definir_escala(self, s):
            self.image = pygame.transform.rotozoom(self.image, 0, s)
            self._escala_actual = s

        def obtener_rotacion(self):
            return 0

        def definir_rotacion(self, r):
            print "pygame no permite cambiar la rotacion"


    def __init__(self):
        import pilas.colores
        pygame.init()
        pilas.colores.gris = (200, 200, 200)

    def crear_ventana(self, ancho, alto, titulo):
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(titulo)
        return self.ventana

    def dibujar_circulo(self, x, y, radio, color, color_borde):
        pygame.draw.circle(self.ventana, (200, 0, 0), (x + 320, 240 - y), radio/2, True)

    def cargar_sonido(self, ruta):
        return Pygame.Sonido(ruta)

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
                self.procesar_evento_teclado(event)

                if event.key == pygame.K_q:
                    import sys
                    sys.exit(0)
            elif event.type == pygame.MOUSEMOTION:
                # Notifica el movimiento del mouse con una señal
                x, y = event.pos
                dx, dy = event.rel
                y = -y
                dy = -dy

                x -= 320
                y += 240

                eventos.mueve_mouse.send("ejecutar", x=x, y=y, dx=dx, dy=dy)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x -= 320
                y -= 240

                if event.button in (4, 5):
                    if event.button == 4:
                        eventos.mueve_rueda.send("ejecutar", delta=1)
                    else:
                        eventos.mueve_rueda.send("ejecutar", delta=-1)
                else:
                    eventos.click_de_mouse.send("ejecutar", button=event.button, x=x, y=-y)

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                x -= 320
                y -= 240

                eventos.termina_click.send("ejecutar", button=event.button, x=x, y=-y)

    def procesar_evento_teclado(self, event):
        eventos.pulsa_tecla.send("ejecutar", code=event.key)

        if event.key == pygame.K_p:
            pilas.mundo.alternar_pausa()
        elif event.key == pygame.K_F12:
            pilas.mundo.alternar_modo_depuracion()

    def actualizar_pantalla(self):
        pygame.display.flip()

    def pintar(self, color):
        self.ventana.fill(color)

    def cargar_imagen(self, ruta):
        # TODO: Optimizar la imagen preservando el canal alpha.
        return pygame.image.load(ruta)

class pySFML:
    import pilas.base


    class Sonido:

        def __init__(self, ruta):
            buff = sf.SoundBuffer()
            buff.LoadFromFile(ruta)
            self.buffer = buff
            self.sonido = sf.Sound(self.buffer)

        def reproducir(self):
            self.sonido.Play()
        
        def Play(self):
            self.reproducir()

    class Actor(pilas.base.BaseActor, sf.Sprite):
        """Representa un objeto visible en pantalla, algo que se ve y tiene posicion.

        Un objeto Actor se tiene que crear siempre indicando la imagen, ya
        sea como una ruta a un archivo como con un objeto Image. Por ejemplo::

            protagonista = Actor("protagonista_de_frente.png")

        es equivalente a:

            imagen = pilas.imagenes.cargar("protagonista_de_frente.png")
            protagonista = Actor(imagen)

        Luego, na vez que ha sido ejecutada la sentencia aparecerá en el centro de
        la pantalla el nuevo actor para que pueda manipularlo. Por ejemplo
        alterando sus propiedades::

            protagonista.x = 100
            protagonista.scale = 2
            protagonista.rotation = 30


        Estas propiedades tambien se pueden manipular mediante
        interpolaciones. Por ejemplo, para aumentar el tamaño del
        personaje de 1 a 5 en 7 segundos::

            protagonista.scale = pilas.interpolar(1, 5, 7)

        Si creas un sprite sin indicar la imagen se cargará
        una por defecto.
        """

        def __init__(self, image="sin_imagen.png"):

            if isinstance(image, str):
                image = pilas.imagenes.cargar(image)

            sf.Sprite.__init__(self, image)
            pilas.base.BaseActor.__init__(self)
            

        def definir_imagen(self, imagen):
            self.SetImage(imagen)

        def dibujar(self, aplicacion):
            aplicacion.Draw(self)

        
        def duplicar(self, **kv):
            duplicado = self.__class__()

            for clave in kv:
                setattr(duplicado, clave, kv[clave])

            return duplicado

        def obtener_ancho(self):
            return self.GetSize()[0]

        def obtener_alto(self):
            return self.GetSize()[1]

        def __str__(self):
            return "<%s en (%d, %d)>" %(self.__class__.__name__, self.x, self.y)

        def obtener_area(self):
            return self.obtener_ancho(), self.obtener_alto()

        def definir_centro(self, x, y):
            self.SetCenter(x, y)

        def obtener_posicion(self):
            x, y = self.GetPosition()
            return x, -y

        def definir_posicion(self, x, y):
            self.SetPosition(x, -y)

        def obtener_escala(self):
            return self.GetScale()[0]

        def definir_escala(self, s):
            self.SetScale(s, s)

        def obtener_rotacion(self):
            return self.GetRotation()

        def definir_rotacion(self, r):
            self.SetRotation(r)

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

    def dibujar_circulo(self, x, y, radio, color, color_borde):
        delta = radio / 2
        circulo = sf.Shape.Circle(0, 0, delta, color, 2, color_borde)
        circulo.SetCenter(0, 0)
        circulo.SetPosition(x, -y)
        self.ventana.Draw(circulo)

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
                self.procesar_evento_teclado(event)

                if event.Key.Code == sf.Key.Q:
                    import sys
                    sys.exit(0)
                    #self.mundo.terminar()

            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal

                x, y = event.MouseMove.X, event.MouseMove.Y

                if x > 0 and y > 0:
                    x, y = self.ventana.ConvertCoords(x, y)
                    y = -y

                    dx = x - self.mouse_x
                    dy = y - self.mouse_y

                    self.mouse_x = x
                    self.mouse_y = y

                    '''
                    print "abs:", x, y
                    print "delta:", dx, dy
                    '''


                    eventos.mueve_mouse.send("ejecutar", x=x, y=y, dx=dx, dy=dy)

            elif event.Type == sf.Event.MouseButtonPressed:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonReleased:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseMove.Y)
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)

    def procesar_evento_teclado(self, event):
        eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

        if event.Key.Code == sf.Key.P:
            pilas.mundo.cambiar_a_modo_pausa()
        elif event.Key.Code == sf.Key.F12:
            pilas.mundo.cambiar_a_modo_depuracion()

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
        return pySFML.Sonido(ruta)

    def cargar_imagen(self, ruta):
        image = sf.Image()
        image.LoadFromFile(ruta)
        return image
