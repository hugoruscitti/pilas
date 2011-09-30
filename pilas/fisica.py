# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas import colores

try:
    import Box2D as box2d
except ImportError:
    print "No esta disponible box2d, se deshabilitara la fisica."

import math

class Fisica(object):
    """Representa un simulador de mundo fisico, usando la biblioteca box2d."""
    
    def __init__(self, area, gravedad=(0, -90)):
        self.area = area
        try:
            self.escenario = box2d.b2AABB()
            self.escenario.lowerBound = (-1000.0, -1000.0)
            self.escenario.upperBound = (1000.0, 1000.0)
            self.gravedad = box2d.b2Vec2(gravedad[0], gravedad[1])
            try:
                self.mundo = box2d.b2World(self.escenario, self.gravedad, True)
            except ValueError:
                print "Solo esta disponible el motor de fisica para box2d 2.0.2b1"
                raise AttributeError("...")
        except AttributeError:
            print "Deshabilitando modulo de fisica (no se encuentra instalado pybox2d en este equipo)"
            self.mundo = None
            return

        self.constante_mouse = None
        self.i = 0
        self.crear_bordes_del_escenario()
        self.figuras_a_eliminar = []

    def crear_bordes_del_escenario(self):
        self.crear_techo(self.area)
        self.crear_suelo(self.area)
        self.crear_paredes(self.area)

    def reiniciar(self):
        for x in self.mundo.bodyList:
            self.mundo.DestroyBody(x)

        self.crear_bordes_del_escenario()

    def capturar_figura_con_el_mouse(self, figura):
        if self.constante_mouse:
            self.cuando_suelta_el_mouse()
        
        self.constante_mouse = ConstanteDeMovimiento(figura)
    
    def cuando_mueve_el_mouse(self, x, y):
        if self.constante_mouse:
            self.constante_mouse.mover(x, y)

    def cuando_suelta_el_mouse(self):
        if self.constante_mouse:
            self.constante_mouse.eliminar()
            self.constante_mouse = None
        
    def actualizar(self, velocidad=1.0):
        if self.mundo:
            self.mundo.Step(velocidad / 20.0, 10, 8)
            self.i += 1
            self._procesar_figuras_a_eliminar()

    def _procesar_figuras_a_eliminar(self):
        "Elimina las figuras que han sido marcadas para quitar."
        if self.figuras_a_eliminar:
            for x in self.figuras_a_eliminar:
                # Solo elimina las figuras que actualmente existen.
                if x in self.mundo.bodyList:
                    self.mundo.DestroyBody(x)
            self.figuras_a_eliminar = []

    def dibujar_figuras_sobre_lienzo(self, motor, lienzo, grosor=1):
        "Dibuja todas las figuras en una pizarra. Indicado para depuracion."
        cuerpos = self.mundo.bodyList
        cantidad_de_figuras = 0
        
        for cuerpo in cuerpos:
            xform = cuerpo.GetXForm()
            
            for figura in cuerpo.shapeList:
                cantidad_de_figuras += 1
                tipo_de_figura = figura.GetType()
                
                if tipo_de_figura == box2d.e_polygonShape:
                    vertices = []
                    
                    for v in figura.vertices:
                        pt = box2d.b2Mul(xform, v)
                        vertices.append((pt.x, pt.y))
                        
                    lienzo.poligono(motor, vertices, color=colores.rojo, grosor=grosor, cerrado=True)
                    
                elif tipo_de_figura == box2d.e_circleShape:
                    lienzo.circulo(motor, cuerpo.position.x, cuerpo.position.y, figura.radius, colores.rojo, grosor=grosor)
                else:
                    print "no puedo identificar el tipo de figura."
        
    def crear_cuerpo(self, definicion_de_cuerpo):
        return self.mundo.CreateBody(definicion_de_cuerpo)
    
    def crear_suelo(self, (ancho, alto), restitucion=0):
        self.suelo = Rectangulo(0, -alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_techo(self, (ancho, alto), restitucion=0):
        self.techo = Rectangulo(0, alto/2, ancho, 2, dinamica=False, fisica=self, restitucion=restitucion)
        
    def crear_paredes(self, (ancho, alto), restitucion=0):
        self.pared_izquierda = Rectangulo(-ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)
        self.pared_derecha = Rectangulo(ancho/2, 0, 2, alto, dinamica=False, fisica=self, restitucion=restitucion)
        
    def eliminar_suelo(self):
        if self.suelo:
            self.suelo.eliminar()
            self.suelo = None

    def eliminar_techo(self):
        if self.techo:
            self.techo.eliminar()
            self.techo = None
            
    def eliminar_paredes(self):
        if self.pared_izquierda:
            self.pared_derecha.eliminar()
            self.pared_izquierda.eliminar()
            self.pared_derecha = None
            self.pared_izquierda = None
    
    def eliminar_figura(self, figura):
        self.figuras_a_eliminar.append(figura)
        
    def obtener_distancia_al_suelo(self, x, y, dy):
        """Obtiene la distancia hacia abajo desde el punto (x,y). 
        
        El valor de 'dy' tiene que ser positivo.
        
        Si la funcion no encuentra obstaculos retornara
        dy, pero en paso contrario retornara un valor menor
        a dy.
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
        "Retorna una lista de cuerpos que se encuentran en la posicion (x, y) o retorna una lista vacia []."

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
        pilas.fisica.definir_gravedad(x, y)

class Figura(object):
    """Representa un figura que simula un cuerpo fisico.
    
    Esta figura es abstracta, no está pensada para crear
    objetos a partir de ella. Se usa como base para el resto
    de las figuras cómo el Circulo o el Rectangulo simplemente."""

    def obtener_x(self):
        return self._cuerpo.position.x

    def definir_x(self, x):
        self._cuerpo.SetXForm((x, self.y), self._cuerpo.GetAngle())

    def obtener_y(self):
        return self._cuerpo.position.y

    def definir_y(self, y):
        self._cuerpo.SetXForm((self.x, y), self._cuerpo.GetAngle())

    def obtener_rotacion(self):
        return - math.degrees(self._cuerpo.GetAngle())

    def definir_rotacion(self, angulo):
        self._cuerpo.SetXForm((self.x, self.y), math.radians(-angulo))
        
    def impulsar(self, dx, dy):
        self._cuerpo.ApplyImpulse((dx, dy), self._cuerpo.GetWorldCenter())
        
    def obtener_velocidad_lineal(self):
        velocidad = self._cuerpo.GetLinearVelocity()
        return (velocidad.x, velocidad.y)

    def detener(self):
        """Hace que la figura regrese al reposo."""
        self.definir_velocidad_lineal(0, 0)

    def definir_velocidad_lineal(self, dx=None, dy=None):
        anterior_dx, anterior_dy = self.obtener_velocidad_lineal()

        if dx is None:
            dx = anterior_dx
        if dy is None:
            dy = anterior_dy

        self._cuerpo.SetLinearVelocity((dx, dy))

    def empujar(self, dx=None, dy=None):
        self.definir_velocidad_lineal(dx, dy)
        
    def eliminar(self):
        """Quita una figura de la simulación."""
        pilas.mundo.fisica.eliminar_figura(self._cuerpo)
        
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
            fisica=None):

        if not fisica:
            fisica = pilas.mundo.fisica
            
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)
        bodyDef.linearDamping = amortiguacion
        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        #self.parent.element_count += 1
        
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        # Add a shape to the Body
        circleDef = box2d.b2CircleDef()
        circleDef.density = densidad
        circleDef.radius = radio
        circleDef.restitution = restitucion
        circleDef.friction = friccion
        
        body.CreateShape(circleDef)
        body.SetMassFromShapes()    

        self._cuerpo = body

class Rectangulo(Figura):
    """Representa un rectángulo que puede colisionar con otras figuras.

    Se puede crear un rectángulo independiente y luego asociarlo
    a un actor de la siguiente forma:

        >>> rect = pilas.fisica.Rectangulo(50, 90, True)
        >>> actor = pilas.actores.Pingu()
        >>> actor.imitar(rect)
    """

    def __init__(self, x, y, ancho, alto, dinamica=True, densidad=1.0, 
            restitucion=0.56, friccion=10.5, amortiguacion=0.1, 
            fisica=None):

        if not fisica:
            fisica = pilas.mundo.fisica

        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)
        bodyDef.linearDamping = amortiguacion
        
        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        #self.parent.element_count += 1
        
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        # Add a shape to the Body
        boxDef = box2d.b2PolygonDef()
        
        boxDef.SetAsBox(ancho/2, alto/2, (0,0), 0)
        boxDef.density = densidad
        boxDef.restitution = restitucion
        boxDef.friction = friccion
        body.CreateShape(boxDef)

        body.SetMassFromShapes()    

        self._cuerpo = body


class Poligono(Figura):
    """Representa un cuerpo poligonal.

    El poligono necesita al menos tres puntos para dibujarse, y cada
    uno de los puntos se tienen que ir dando en orden de las agujas
    del relog.

    Por ejemplo:

        >>> pilas.fisica.Poligono([(100, 2), (-50, 0), (-100, 100.0)])
        
    """
    
    def __init__(self, puntos, dinamica=True, densidad=1.0, 
            restitucion=0.56, friccion=10.5, amortiguacion=0.1, 
            fisica=None):

        if not fisica:
            fisica = pilas.mundo.fisica
            
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=puntos[0]
        bodyDef.linearDamping = amortiguacion
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        if len(puntos) < 3:
            raise Exception("Tienes que definir al menos 3 puntos para tener un poligono")

        # Add a shape to the Body
        poligono_def = box2d.b2PolygonDef()
        puntos.reverse()
        poligono_def.setVertices(puntos)

        poligono_def.density = densidad
        poligono_def.restitution = restitucion
        poligono_def.friction = friccion
        #poligono_def.setVertices(puntos)
        #poligono_def.vertexCount = len(puntos)

        #for indice, punto in enumerate(puntos):
        #    poligono_def.setVertex(indice, punto[0], punto[1])
        #    #poligono_def.vertices[indice] = punto
        
        body.CreateShape(poligono_def)
        body.SetMassFromShapes()
        self._cuerpo = body

class ConstanteDeMovimiento():

    def __init__(self, figura):
        md = box2d.b2MouseJointDef()
        mundo = pilas.mundo.fisica.mundo
        md.body1 = mundo.GetGroundBody()
        md.body2 = figura._cuerpo
        md.target = (figura.x, figura.y)
        md.maxForce = 5000.0 * figura._cuerpo.GetMass()

        try:
            self.constante = mundo.CreateJoint(md).getAsType()
        except:
            self.constante = mundo.CreateJoint(md)

        figura._cuerpo.WakeUp()

    def mover(self, x, y):
        self.constante.SetTarget((x, y))

    def eliminar(self):
        pilas.mundo.fisica.mundo.DestroyJoint(self.constante)

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

    def __init__(self, figura_1, figura_2, fisica=None):
        if not fisica:
            fisica = pilas.mundo.fisica
            
        if not isinstance(figura_1, Figura) or not isinstance(figura_2, Figura):
            raise Exception("Las dos figuras tienen que ser objetos de la clase Figura.")
        
        constante = box2d.b2DistanceJointDef()
        constante.Initialize(figura_1._cuerpo, figura_2._cuerpo, (0,0), (0,0))
        constante.collideConnected = True
        self.constante = fisica.mundo.CreateJoint(constante)


    def eliminar(self):
        pilas.mundo.fisica.mundo.DestroyJoint(self.constante_mouse)

def definir_gravedad(x=0, y=-90):
    pilas.mundo.fisica.mundo.gravity = (x, y)
