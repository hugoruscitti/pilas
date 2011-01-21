# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pygame
from pilas.simbolos import *
import cairo
import pilas
from pilas import eventos

ANCHO = 640
ALTO = 480

"""pilas.baseactor.BaseActor,""" 
class PygameActor(pygame.sprite.Sprite):
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

    def __init__(self, image="sin_imagen.png", x=0, y=0):
        self.centro_x = 0
        self.centro_y = 0

        if isinstance(image, str):
            image = pilas.imagenes.cargar(image)

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_original = image.convert_alpha()
        self.rect = self.image.get_rect()
        self._escala_actual = 1
        self._rotacion_actual = 0
        
    def definir_imagen(self, imagen):
        self.image = imagen

        if self._rotacion_actual:
            self.rotacion = self._rotacion_actual

    def obtener_imagen(self):
        return self.image

    def dibujar(self, aplicacion):
        x, y = self.rect.topleft
        aplicacion.blit(self.image, (x + 320 - self.centro_x - pilas.motor.camara_x, 
                y + 240 - self.centro_y - pilas.motor.camara_y))

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
        self.centro_x = x
        self.centro_y = y

    def obtener_posicion(self):
        x, y = self.rect.topleft
        return x, -y

    def definir_posicion(self, x, y):
        self.rect.topleft = (x, -y)

    def obtener_escala(self):
        return self._escala_actual

    def definir_escala(self, s):
        self.image = pygame.transform.rotozoom(self.image, 0, s)
        self._escala_actual = s

    def obtener_rotacion(self):
        return self._rotacion_actual

    def definir_rotacion(self, r):
        self.image = pygame.transform.rotozoom(self.image_original, -r, 1)
        self._rotacion_actual = r

        # Se asegura que el personaje gire desde el centro
        # del area de colision.
        centro = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = centro

class Pygame:
    """Representa la capa de interaccion con la biblioteca Pygame.

    Esto permite que tus juegos realizados con pilas funcionen
    en cualquier equipo que tenga instalada la biblioteca pygame,
    por ejemplo equipos como OLPC o simplemente aquellos que no
    tengan aceleradoras de graficos OpenGL."""

    import pilas.baseactor

    class Color(pygame.Color):

        def obtener_componentes(self):
            return (self.r, self.g, self.b)

    class Canvas:
        "Representa una superficie sobre la que se puede dibujar usando cairo."

        def __init__(self):
            import array
            self.data = array.array('c', chr(0) * ANCHO * ALTO * 4)
            stride = ANCHO * 4
            self.surface = cairo.ImageSurface.create_for_data(self.data, cairo.FORMAT_ARGB32, 
                    ANCHO, ALTO, stride)

            self.context = cairo.Context(self.surface)
            self.actualizar()

        def actualizar(self):
            #self.image.LoadFromPixels(ANCHO, ALTO, self.surface.get_data())
            self.image = pygame.image.frombuffer(self.data.tostring(), (ANCHO, ALTO), "RGBA")
            
        def limpiar(self):
            import array
            self.data = array.array('c', chr(0) * ANCHO * ALTO * 4)
            stride = ANCHO * 4
            self.surface = cairo.ImageSurface.create_for_data(self.data, cairo.FORMAT_ARGB32, 
                    ANCHO, ALTO, stride)

            self.context = cairo.Context(self.surface)
            
    class Grilla:
        """Representa una grilla de imagenes con varios cuadros de animación.

        Una grilla es un objeto que se tiene que inicializar con la ruta
        a una imagen, la cantidad de columnas y filas.

        Por ejemplo, si tenemos una grilla con 2 columnas y 3 filas
        podemos asociarla a un actor de la siguiente manera::

            grilla = pilas.imagenes.Grilla("animacion.png", 2, 3)
            grilla.asignar(actor)

        Entonces, a partir de ahora nuestro actor muestra solamente un
        cuadro de toda la grilla.

        Si quieres avanzar la animacion tienes que modificar el objeto
        grilla y asignarlo nuevamente al actor::

            grilla.avanzar()
            grilla.asignar(actor)
        """

        def __init__(self, ruta, columnas=1, filas=1):
            self.image = pilas.imagenes.cargar(ruta)
            self.cantidad_de_cuadros = columnas * filas
            self.columnas = columnas
            self.filas = filas
            self.cuadro_ancho = self.image.get_width() / columnas
            self.cuadro_alto = self.image.get_height() / filas
            self.crear_grilla_de_imagenes()
            self.definir_cuadro(0)

        def crear_grilla_de_imagenes(self):
            "Genera una lista con los cuadros de animación en una grilla"
                                
            tile_w = self.cuadro_ancho
            tile_h = self.cuadro_alto
            self.imagenes = []

            for c in range(self.columnas):
                for r in range(self.filas):
                    rect = pygame.Rect(c * (tile_w) , r * (tile_h), tile_w, tile_h)
                    self.imagenes.append(self.image.subsurface(rect).copy())


        def definir_cuadro(self, cuadro):
            self.cuadro = cuadro

            '''
            frame_col = cuadro % self.columnas
            frame_row = cuadro / self.columnas

            dx = frame_col * self.cuadro_ancho - self.sub_rect.Left
            dy = frame_row * self.cuadro_alto - self.sub_rect.Top
            '''

            #self.sub_rect.Offset(dx, dy)

        def asignar(self, sprite):
            "Sets the sprite's image with animation state."

            cuadro_de_imagen = self.imagenes[self.cuadro]
            sprite.definir_imagen(cuadro_de_imagen)
            sprite.rect.width = cuadro_de_imagen.get_width()
            sprite.rect.height = cuadro_de_imagen.get_height()

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

    class Sonido:

        def __init__(self, ruta):
            self.sonido = pygame.mixer.Sound(ruta)

        def reproducir(self):
            self.sonido.play()
        
        def Play(self):
            self.reproducir()


    """pilas.baseactor.BaseActor,""" 

    class Texto(pygame.sprite.Sprite):
        """Representa un texto en pantalla.

        El texto tiene atributos como ``texto``, ``magnitud`` y ``color``.
        """

        def __init__(self, texto="None", x=0, y=0):
            self.centro_x = 0
            self.centro_y = 0
            pygame.font.init()
            self.font = pygame.font.Font(None, 32)
            self._color = pilas.colores.negro

            pygame.sprite.Sprite.__init__(self)
            self.set_text(texto)
            self.rect = self.image.get_rect()
            pilas.baseactor.BaseActor.__init__(self, x=x, y=y) 
            self._escala_actual = 1
            self._texto = texto

        def get_text(self):
            return self._texto

        def set_text(self, texto):
            self._texto = texto
            self.image = self.font.render(texto, 1, self.color.obtener_componentes())

        def get_size(self):
            return 32

        def set_size(self, size):
            print "No se puede cambiar el tamanano del texto en pygame"

        '''
        def _set_central_axis(self):
            rect = self.GetRect()
            size = (rect.GetWidth(), rect.GetHeight())
            self.SetCenter(size[0]/2, size[1]/2)
        '''

        def obtener_posicion(self):
            x, y = self.rect.topleft
            return x, y

        def definir_posicion(self, x, y):
            self.rect.topleft = (x, -y)

        def get_color(self):
            return self._color

        def set_color(self, k):
            self._color = k
            self.texto = self._texto

        texto = property(get_text, set_text, doc="El texto que se tiene que mostrar.")
        magnitud = property(get_size, set_size, doc="El tamaño del texto.")
        color = property(get_color, set_color, doc="Color del texto.")

        def dibujar(self, aplicacion):
            x, y = self.rect.topleft
            #aplicacion.blit(self.image, (x + 320 - self.centro_x, y + 240 - self.centro_y))
            aplicacion.blit(self.image, (x + 320 - self.centro_x - pilas.motor.camara_x, 
                    y + 240 - self.centro_y - pilas.motor.camara_y))

        def colisiona_con_un_punto(self, x, y):
            return False

        def obtener_ancho(self):
            return self.rect.width

        def obtener_alto(self):
            return self.rect.height

        def obtener_area(self):
            return self.obtener_ancho(), self.obtener_alto()

        def definir_centro(self, x, y):
            self.centro_x = x
            self.centro_y = y


    def __init__(self):
        pygame.init()

        if pygame.image.get_extended() != 1:
            print "Cuidado, en este equipo pygame no soporta archivos PNG. Instale SDL_image para resolver este problema."

        self.camara_x = 0
        self.camara_y = 0

    def crear_ventana(self, ancho, alto, titulo):
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(titulo)
        return self.ventana

    def cerrar_ventana(self):
        pygame.display.quit()

    def dibujar_circulo(self, x, y, radio, color, color_borde):
        pygame.draw.circle(self.ventana, (200, 0, 0), (x + 320 - pilas.motor.camara_x, 
            240 - y - pilas.motor.camara_y), radio/2, True)
        #aplicacion.blit(self.image, (x + 320 - self.centro_x - pilas.motor.camara_x, 
        #        y + 240 - self.centro_y - pilas.motor.camara_y))


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
                SELECCION: pygame.K_RETURN,
                }

        return pygame.key.get_pressed()[mapa[tecla]]

    def procesar_y_emitir_eventos(self):
        "Procesa todos los eventos que la biblioteca pygame pone en una cola."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pilas.mundo.terminar()
            elif event.type == pygame.KEYDOWN:
                self.procesar_evento_teclado(event)

                if event.key == pygame.K_q:
                    pilas.mundo.terminar()
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
        eventos.pulsa_tecla.send("ejecutar", codigo=event.unicode)

        if event.key == pygame.K_p:
            pilas.mundo.alternar_pausa()
        elif event.key == pygame.K_F12:
            pilas.mundo.alternar_modo_depuracion()
        elif event.key == pygame.K_ESCAPE:
            eventos.pulsa_tecla_escape.send("ejecutar")


    def actualizar_pantalla(self):
        pygame.display.flip()

    def ocultar_puntero_del_mouse(self):
        pygame.mouse.set_visible(True)

    def mostrar_puntero_del_mouse(self):
        pygame.mouse.set_visible(False)

    def pintar(self, color):
        self.ventana.fill((color.r, color.g, color.b))

    def cargar_imagen(self, ruta):
        # TODO: Optimizar la imagen preservando el canal alpha.
        return pygame.image.load(ruta)

    def obtener_centro_de_la_camara(self):
        return self.camara_x, self.camara_y

    def definir_centro_de_la_camara(self, x, y):
        self.camara_x, self.camara_y = x, y


    def generar_imagen_cairo(self, imagen):
        """Retorna una superficie de cairo representando a la imagen.

        Esta funcion es util para pintar imagenes sobre una pizarra
        o el escenario de un videojuego.
        """
        #import array

        pixels = imagen.get_buffer()
        w = imagen.get_width()
        h = imagen.get_height()

        return cairo.ImageSurface.create_for_data(pixels, cairo.FORMAT_RGB24, w, h)

    def obtener_actor(self, imagen, x, y):
        return PygameActor(imagen, x, y)
