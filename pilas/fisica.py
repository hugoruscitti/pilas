# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

PPM = 30

import math
import pilas

try:
    import Box2D as box2d
    contact_listener = box2d.b2ContactListener
    __enabled__ = True
except ImportError:
    __enabled__ = False
    class Tmp:
        pass
    contact_listener = Tmp


def convertir_a_metros(valor):
    """Convierte una magnitid de pixels a metros."""
    return valor / float(PPM)

def convertir_a_pixels(valor):
    """Convierte una magnitud de metros a pixels."""
    return valor * PPM


def crear_motor_fisica(area, gravedad):
    """Genera el motor de física Box2D.

    :param area: El area de juego.
    :param gravedad: La gravedad del escenario.
    """
    if __enabled__:
        if obtener_version().startswith('2.0'):
            print "Los siento, el soporte para Box2D version 2.0 se ha eliminado."
            print "Por favor actualice Box2D a la version 2.1 (ver http://www.pilas-engine.com.ar)."
            return FisicaDeshabilitada(area, gravedad)
        else:
            return Fisica(area, gravedad)
    else:
        print "No se pudo iniciar Box2D, se deshabilita el soporte de Fisica."
        return FisicaDeshabilitada(area, gravedad)

def obtener_version():
    """Obtiene la versión de la biblioteca Box2D"""
    return box2d.__version__

def obtener_version_en_tupla():
    """Obtiene la versión de la biblioteca Box2D"""
    return box2d.__version_info__

class Fisica(object):
    """Representa un simulador de mundo fisico, usando la biblioteca Box2D (version 2.1)."""

    def __init__(self, area, gravedad):
        """Inicializa el motor de física.

        :param area: El area del escenario, en forma de tupla.
        :param gravedad: La aceleración del escenario.
        """
        self.mundo = box2d.b2World(gravedad, False)
        self.objetosContactListener = ObjetosContactListener()
        self.mundo.contactListener = self.objetosContactListener
        self.mundo.continuousPhysics = False

        self.area = area
        self.figuras_a_eliminar = []

        self.constante_mouse = None
        self.crear_bordes_del_escenario()

        self.velocidad = 1.0
        self.timeStep = self.velocidad/120.0

    def crear_bordes_del_escenario(self):
        """Genera las paredes, el techo y el suelo."""
        self.crear_techo(self.area)
        self.crear_suelo(self.area)
        self.crear_paredes(self.area)

    def reiniciar(self):
        """Elimina todos los objetos físicos y vuelve a crear el entorno."""
        lista = list(self.mundo.bodies)

        for x in lista:
            self.mundo.DestroyBody(x)

        self.crear_bordes_del_escenario()

    def capturar_figura_con_el_mouse(self, figura):
        """Comienza a capturar una figura con el mouse.

        :param figura: La figura a controlar con el mouse.
        """
        if self.constante_mouse:
            self.cuando_suelta_el_mouse()

        self.constante_mouse = ConstanteDeMovimiento(figura)

    def cuando_mueve_el_mouse(self, x, y):
        """Gestiona el evento de movimiento del mouse.

        :param x: Coordenada horizontal del mouse.
        :param y: Coordenada vertical del mouse.
        """
        if self.constante_mouse:
            self.constante_mouse.mover(x, y)

    def cuando_suelta_el_mouse(self):
        """Se ejecuta cuando se suelta el botón de mouse."""
        if self.constante_mouse:
            self.constante_mouse.eliminar()
            self.constante_mouse = None

    def actualizar(self, velocidad=1.0):
        """Realiza la actualización lógica del escenario.
        """
        # TODO: eliminar el arguemnto velocidad que no se utiliza.
        if self.mundo:
            self.mundo.Step(self.timeStep, 6, 3)
            self._procesar_figuras_a_eliminar()
            self.mundo.ClearForces()

    def pausar_mundo(self):
        """Detiene la simulación física."""
        if self.mundo:
            self.timeStep = 0

    def reanudar_mundo(self):
        """Restaura la simulación física."""
        if self.mundo:
            self.timeStep = self.velocidad/120.0

    def _procesar_figuras_a_eliminar(self):
        "Elimina las figuras que han sido marcadas para quitar."
        if self.figuras_a_eliminar:
            for x in self.figuras_a_eliminar:
                # Solo elimina las figuras que actualmente existen.
                if x in self.mundo.bodies:
                    self.mundo.DestroyBody(x)
            self.figuras_a_eliminar = []

    def dibujar_figuras_sobre_lienzo(self, motor, lienzo, grosor=1):
        """Dibuja todas las figuras en una pizarra. Indicado para depuracion.

        :param motor: Referencia al motor de pilas.
        :param lienzo: Un actor lienzo sobre el que se dibujará.
        :param grosor: El grosor de la linea medida en pixels.
        """

        cuerpos = self.mundo.bodies

        for cuerpo in cuerpos:

            for fixture in cuerpo:

                # cuerpo.type == 0 → estatico
                # cuerpo.type == 1 → kinematico
                # cuerpo.type == 2 → dinamico

                shape = fixture.shape

                if isinstance(shape, box2d.b2PolygonShape):
                    vertices = [cuerpo.transform * v * PPM for v in shape.vertices]
                    vertices = [pilas.escena_actual().camara.desplazar(v) for v in vertices]
                    lienzo.poligono(motor, vertices, color=pilas.colores.blanco, grosor=grosor, cerrado=True)
                elif isinstance(shape, box2d.b2CircleShape):
                    (x, y) = pilas.escena_actual().camara.desplazar(cuerpo.transform * shape.pos * PPM)

                    lienzo.circulo(motor, x, y, shape.radius * PPM, pilas.colores.blanco, grosor=grosor)
                else:
                    # TODO: implementar las figuras de tipo "edge" y "loop".
                    raise Exception("No puedo identificar el tipo de figura.")


    def crear_cuerpo(self, definicion_de_cuerpo):
        """Genera un Body de box2d.

        :param definicion_de_cuerpo: Los parámetros de configuración de un cuerpo para Box2d.
        """
        return self.mundo.CreateBody(definicion_de_cuerpo)

    def crear_suelo(self, (ancho, alto), restitucion=0):
        """Genera un suelo sólido para el escenario.

        :param ancho: El ancho del suelo.
        :param alto: Alto del suelo.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.suelo = Rectangulo(0, -alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_techo(self, (ancho, alto), restitucion=0):
        """Genera un techo sólido para el escenario.

        :param ancho: El ancho del techo.
        :param alto: Alto del techo.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.techo = Rectangulo(0, alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_paredes(self, (ancho, alto), restitucion=0):
        """Genera dos paredes para el escenario.

        :param ancho: El ancho de las paredes.
        :param alto: El alto de las paredes.
        :param restitucion: El grado de conservación de energía ante una colisión.
        """
        self.pared_izquierda = Rectangulo(-ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)
        self.pared_derecha = Rectangulo(ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)

    def eliminar_suelo(self):
        "Elimina el suelo del escenario."
        if self.suelo:
            self.suelo.eliminar()
            self.suelo = None

    def eliminar_techo(self):
        "Elimina el techo del escenario."
        if self.techo:
            self.techo.eliminar()
            self.techo = None

    def eliminar_paredes(self):
        "Elimina las dos paredes del escenario."
        if self.pared_izquierda:
            self.pared_derecha.eliminar()
            self.pared_izquierda.eliminar()
            self.pared_derecha = None
            self.pared_izquierda = None

    def eliminar_figura(self, figura):
        """Elimina una figura del escenario.

        :param figura: Figura a eliminar.
        """
        self.figuras_a_eliminar.append(figura)

    def obtener_distancia_al_suelo(self, x, y, dy):
        """Obtiene la distancia hacia abajo desde el punto (x,y).

        El valor de 'dy' tiene que ser positivo.

        Si la funcion no encuentra obstaculos retornara
        dy, pero en paso contrario retornara un valor menor
        a dy.

        :param x: posición horizontal del punto a analizar.
        :param y: posición vertical del punto a analizar.
        """

        if dy < 0:
            raise Exception("El valor de 'dy' debe ser positivo, ahora vale '%f'." %(dy))

        delta = 0

        while delta < dy:

            if self.obtener_cuerpos_en(x, y-delta):
                return delta

            delta += 1

        return delta

    def obtener_cuerpos_en(self, x, y):
        """Retorna una lista de cuerpos que se encuentran en la posicion (x, y) o retorna una lista vacia [].

        :param x: posición horizontal del punto a analizar.
        :param y: posición vertical del punto a analizar.
        """

        AABB = box2d.b2AABB()
        f = 1
        AABB.lowerBound = (x-f, y-f)
        AABB.upperBound = (x+f, y+f)

        cuantos, cuerpos = self.mundo.Query(AABB, 2)

        if cuantos == 0:
            return []

        lista_de_cuerpos = []

        for s in cuerpos:
            cuerpo = s.GetBody()

            if s.TestPoint(cuerpo.GetXForm(), (x, y)):
                lista_de_cuerpos.append(cuerpo)

        return lista_de_cuerpos

    def definir_gravedad(self, x, y):
        """Define la gravedad del motor de física.

        :param x: Aceleración horizontal.
        :param y: Aceleración vertical.
        """
        pilas.fisica.definir_gravedad(x, y)

class FisicaDeshabilitada(object):
    """Representa a un motor de física que no realiza acciones, y solo se habilita si box2d
    no funciona en el equipo.
    """

    def __init__(self, area, gravedad=None):
        pass

    def actualizar(self):
        pass

    def dibujar_figuras_sobre_lienzo(self, motor, lienzo, grosor=1):
        pass
    def crear_bordes_del_escenario(self):
        pass

    def reiniciar(self):
        pass

    def capturar_figura_con_el_mouse(self, figura):
        pass

    def cuando_mueve_el_mouse(self, x, y):
        pass

    def cuando_suelta_el_mouse(self):
        pass

    def pausar_mundo(self):
        pass

    def reanudar_mundo(self):
        pass

    def dibujar_figuras_sobre_lienzo(self, motor, lienzo, grosor=1):
        pass

    def crear_cuerpo(self, definicion_de_cuerpo):
        pass

    def crear_suelo(self, (ancho, alto), restitucion=0):
        pass

    def crear_techo(self, (ancho, alto), restitucion=0):
        pass

    def crear_paredes(self, (ancho, alto), restitucion=0):
        pass

    def eliminar_suelo(self):
        pass

    def eliminar_techo(self):
        pass

    def eliminar_paredes(self):
        pass

    def obtener_distancia_al_suelo(self, x, y, dy):
        pass

    def eliminar_figura(self, figura):
        pass

    def obtener_cuerpos_en(self, x, y):
        pass

    def definir_gravedad(self, x, y):
        pass


class Figura(object):
    """Representa un figura que simula un cuerpo fisico.

    Esta figura es abstracta, no está pensada para crear
    objetos a partir de ella. Se usa como base para el resto
    de las figuras cómo el Circulo o el Rectangulo simplemente."""

    def __init__(self):
        self.id = pilas.utils.obtener_uuid()

    def obtener_x(self):
        "Retorna la posición horizontal del cuerpo."
        return convertir_a_pixels(self._cuerpo.position.x)

    def definir_x(self, x):
        """Define la posición horizontal del cuerpo.

        :param x: El valor horizontal a definir.
        """
        self._cuerpo.position.x = convertir_a_metros(x)

    def obtener_y(self):
        "Retorna la posición vertical del cuerpo."
        return convertir_a_pixels(self._cuerpo.position.y)

    def definir_y(self, y):
        """Define la posición vertical del cuerpo.

        :param y: El valor vertical a definir.
        """
        self._cuerpo.position.y = convertir_a_metros(y)

    def definir_posicion(self, x, y):
        """Define la posición para el cuerpo.

        :param x: Posición horizontal que se asignará al cuerpo.
        :param y: Posición vertical que se asignará al cuerpo.
        """
        self.definir_x(x)
        self.definir_y(y)

    def obtener_rotacion(self):
        return - math.degrees(self._cuerpo.angle)

    def definir_rotacion(self, angulo):
        # TODO: simplificar a la nueva api.
        self._cuerpo.SetXForm((self.x, self.y), math.radians(-angulo))

    def impulsar(self, dx, dy):
        # TODO: convertir los valores dx y dy a metros.
        self._cuerpo.ApplyLinearImpulse((dx, dy), (0, 0))

    def obtener_velocidad_lineal(self):
        # TODO: convertir a pixels
        velocidad = self._cuerpo.linearVelocity
        return (velocidad.x, velocidad.y)

    def detener(self):
        """Hace que la figura regrese al reposo."""
        self.definir_velocidad_lineal(0, 0)

    def definir_velocidad_lineal(self, dx=None, dy=None):
        # TODO: convertir a metros
        anterior_dx, anterior_dy = self.obtener_velocidad_lineal()

        if dx is None:
            dx = anterior_dx
        if dy is None:
            dy = anterior_dy

        b2vec = self._cuerpo.linearVelocity
        b2vec.x = dx
        b2vec.y = dy

        # Añadimos eltry, porque aparece el siguiente error:
        # TypeError: in method 'b2Vec2___call__', argument 2 of type 'int32'
        try:
            self._cuerpo.linearVelocity(b2vec)
        except:
            pass

    def empujar(self, dx=None, dy=None):
        # TODO: convertir a metros???
        self.definir_velocidad_lineal(dx, dy)

    def eliminar(self):
        """Quita una figura de la simulación."""
        pilas.escena_actual().fisica.eliminar_figura(self._cuerpo)

    x = property(obtener_x, definir_x, doc="define la posición horizontal.")
    y = property(obtener_y, definir_y, doc="define la posición vertical.")
    rotacion = property(obtener_rotacion, definir_rotacion, doc="define la rotacion.")

class Circulo(Figura):
    """Representa un cuerpo de circulo.

    Generalmente estas figuras se pueden construir independientes de un
    actor, y luego asociar.

    Por ejemplo, podríamos crear un círculo:

        >>> circulo_dinamico = pilas.fisica.Circulo(10, 200, 50)

    y luego tomar un actor cualquiera, y decirle que se comporte
    cómo el circulo:

        >>> mono = pilas.actores.Mono()
        >>> mono.imitar(circulo_dinamico)
    """

    def __init__(self, x, y, radio, dinamica=True, densidad=1.0,
            restitucion=0.56, friccion=10.5, amortiguacion=0.1,
            fisica=None, sin_rotacion=False):

        Figura.__init__(self)

        x = convertir_a_metros(x)
        y = convertir_a_metros(y)
        radio = convertir_a_metros(radio)

        if not fisica:
            fisica = pilas.escena_actual().fisica

        if not dinamica:
            densidad = 0

        fixture = box2d.b2FixtureDef(shape=box2d.b2CircleShape(radius=radio),
                                     density=densidad,
                                     linearDamping=amortiguacion,
                                     friction=friccion,
                                     restitution=restitucion)

        # Agregamos un identificador para controlarlo posteriormente en las
        # colisiones.
        userData = { 'id' : self.id }
        fixture.userData = userData

        if dinamica:
            self._cuerpo = fisica.mundo.CreateDynamicBody(position=(x, y), fixtures=fixture)
        else:
            self._cuerpo = fisica.mundo.CreateKinematicBody(position=(x, y), fixtures=fixture)

        self._cuerpo.fixedRotation = sin_rotacion

class Rectangulo(Figura):
    """Representa un rectángulo que puede colisionar con otras figuras.

    Se puede crear un rectángulo independiente y luego asociarlo
    a un actor de la siguiente forma:

        >>> rect = pilas.fisica.Rectangulo(50, 90, True)
        >>> actor = pilas.actores.Pingu()
        >>> actor.imitar(rect)
    """

    def __init__(self, x, y, ancho, alto, dinamica=True, densidad=1.0,
            restitucion=0.5, friccion=.2, amortiguacion=0.1,
            fisica=None, sin_rotacion=False):

        Figura.__init__(self)

        x = convertir_a_metros(x)
        y = convertir_a_metros(y)
        ancho = convertir_a_metros(ancho)
        alto = convertir_a_metros(alto)

        if not fisica:
            fisica = pilas.escena_actual().fisica

        if not dinamica:
            densidad = 0

        fixture = box2d.b2FixtureDef(shape=box2d.b2PolygonShape(box=(ancho/2, alto/2)),
                                     density=densidad,
                                     linearDamping=amortiguacion,
                                     friction=friccion,
                                     restitution=restitucion)

        # Agregamos un identificador para controlarlo posteriormente en las
        # colisiones.
        userData = { 'id' : self.id }
        fixture.userData = userData

        if dinamica:
            self._cuerpo = fisica.mundo.CreateDynamicBody(position=(x, y), fixtures=fixture)
        else:
            self._cuerpo = fisica.mundo.CreateKinematicBody(position=(x, y), fixtures=fixture)

        self._cuerpo.fixedRotation = sin_rotacion


class Poligono(Figura):
    """Representa un cuerpo poligonal.

    El poligono necesita al menos tres puntos para dibujarse, y cada
    uno de los puntos se tienen que ir dando en orden de las agujas
    del relog.

    Por ejemplo:

        >>> pilas.fisica.Poligono([(100, 2), (-50, 0), (-100, 100.0)])

    """

    def __init__(self, x, y, puntos, dinamica=True, densidad=1.0,
            restitucion=0.56, friccion=10.5, amortiguacion=0.1,
            fisica=None, sin_rotacion=False):

        Figura.__init__(self)

        if not fisica:
            fisica = pilas.escena_actual().fisica

        vertices = [(convertir_a_metros(x1), convertir_a_metros(y1)) for (x1, y1) in puntos]

        fixture = box2d.b2FixtureDef(shape=box2d.b2PolygonShape(vertices=vertices),
                                     density=densidad,
                                     linearDamping=amortiguacion,
                                     friction=friccion,
                                     restitution=restitucion)

        userData = { 'id' : self.id }
        fixture.userData = userData

        if dinamica:
            self._cuerpo = fisica.mundo.CreateDynamicBody(position=(0, 0), fixtures=fixture)
        else:
            self._cuerpo = fisica.mundo.CreateKinematicBody(position=(0, 0), fixtures=fixture)

        self._cuerpo.fixedRotation = sin_rotacion


class ConstanteDeMovimiento():
    """Representa una constante de movimiento para el mouse."""

    def __init__(self, figura):
        """Inicializa la constante.

        :param figura: Figura a controlar desde el mouse.
        """
        mundo = pilas.escena_actual().fisica.mundo
        punto_captura = convertir_a_metros(figura.x), convertir_a_metros(figura.y)
        self.cuerpo_enlazado = mundo.CreateBody()
        self.figura_cuerpo = figura
        self.constante = mundo.CreateMouseJoint(bodyA=self.cuerpo_enlazado,
                bodyB=figura._cuerpo,
                target=punto_captura,
                maxForce=1000.0*figura._cuerpo.mass)

        figura._cuerpo.awake = True

    def mover(self, x, y):
        """Realiza un movimiento de la figura.

        :param x: Posición horizontal.
        :param y: Posición vertical.
        """
        self.constante.target = (convertir_a_metros(x), convertir_a_metros(y))

    def eliminar(self):
        # Si se intenta destruir un Joint de un cuerpo que ya no existe, se cierra
        # la aplicación.
        #pilas.escena_actual().fisica.mundo.DestroyJoint(self.constante)
        pilas.escena_actual().fisica.mundo.DestroyBody(self.cuerpo_enlazado)

class ConstanteDeDistancia():
    """Representa una distancia fija entre dos figuras.

    Esta constante es útil para representar ejes o barras
    que sostienen dos cuerpos. Por ejemplo, un eje entre dos
    ruedas en un automóvil:

        >>> circulo_1 = pilas.fisica.Circulo(-100, 0, 50)
        >>> circulo_2 = pilas.fisica.Circulo(100, 50, 50)
        >>> barra = pilas.fisica.ConstanteDeDistancia(circulo_1, circulo_2)

    La distancia que tiene que respetarse en la misma que tienen
    las figuras en el momento en que se establece la constante.
    """

    def __init__(self, figura_1, figura_2, fisica=None, con_colision=True):
        """Inicializa la constante.

        :param figura_1: Una de las figuras a conectar por la constante.
        :param figura_2: La otra figura a conectar por la constante.
        :param fisica: Referencia al motor de física.
        :param con_colision: Indica si se permite colisión entre las dos figuras.
        """
        if not fisica:
            fisica = pilas.escena_actual().fisica

        if not isinstance(figura_1, Figura) or not isinstance(figura_2, Figura):
            raise Exception("Las dos figuras tienen que ser objetos de la clase Figura.")

        constante = box2d.b2DistanceJointDef()
        constante.Initialize(figura_1._cuerpo, figura_2._cuerpo, (0,0), (0,0))
        constante.collideConnected = con_colision
        self.constante = fisica.mundo.CreateJoint(constante)

    def eliminar(self):
        pilas.escena_actual().fisica.mundo.DestroyJoint(self.constante_mouse)

def definir_gravedad(x, y):
    """Define la gravedad del motor de física.

    :param x: Aceleración horizontal.
    :param y: Aceleración vertical.
    """
    pilas.escena_actual().fisica.mundo.gravity = (x, y)

class ObjetosContactListener(contact_listener):
    """Gestiona las colisiones de los objetos para ejecutar funcionés."""

    def __init__(self):
        box2d.b2ContactListener.__init__(self)

    def BeginContact(self, *args, **kwargs):
        objeto_colisionado_1 = args[0].fixtureA
        objeto_colisionado_2 = args[0].fixtureB

        if (not objeto_colisionado_1.userData == None) and (not objeto_colisionado_2.userData == None):
            pilas.escena_actual().colisiones.verificar_colisiones_fisicas(objeto_colisionado_1.userData['id'],
                                                                          objeto_colisionado_2.userData['id'])

