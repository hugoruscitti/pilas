# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import Box2D as box2d
import math


class Fisica(object):
    "Representa un simulador de mundo fisico, usando la biblioteca box2d."
    
    def __init__(self, gravedad=(0, -90)):
        self.escenario = box2d.b2AABB()
        self.escenario.lowerBound = (-1000.0, -1000.0)
        self.escenario.upperBound = (1000.0, 1000.0)
        self.gravedad = box2d.b2Vec2(gravedad[0], gravedad[1])
        self.mundo = box2d.b2World(self.escenario, self.gravedad, True)
        self.i = 0
        self.crear_techo()
        self.crear_suelo()
        self.crear_paredes()
        self.figuras_a_eliminar = []
        
    def actualizar(self):
        self.mundo.Step(1.0 / 20.0, 10, 8)
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

        
    def dibujar_figuras_sobre_pizarra(self, pizarra):
        "Dibuja todas las figuras en una pizarra. Indicado para depuracion."
        cuerpos = self.mundo.bodyList
        cantidad_de_figuras = 0
        
        pizarra.definir_color(pilas.colores.amarillo)
        
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
                        
                    pizarra.dibujar_poligono(vertices)
                    
                elif tipo_de_figura == box2d.e_circleShape:
                    pizarra.dibujar_circulo(cuerpo.position.x, cuerpo.position.y, figura.radius, False)
                else:
                    print "no puedo identificar el tipo de figura."
        
    def crear_cuerpo(self, definicion_de_cuerpo):
        return self.mundo.CreateBody(definicion_de_cuerpo)
    
    def crear_suelo(self, restitucion=1):
        self.suelo = Rectangulo(0, -240, 640, 2, dinamica=False, fisica=self, restitucion=restitucion)

    def crear_techo(self, restitucion=1):
        self.suelo = Rectangulo(0, 240, 640, 2, dinamica=False, fisica=self, restitucion=restitucion)
        
    def crear_paredes(self, restitucion=1):
        self.pared_izquierda = Rectangulo(-320, 0, 2, 480, dinamica=False, fisica=self, restitucion=restitucion)
        self.pared_derecha = Rectangulo(320, 0, 2, 480, dinamica=False, fisica=self, restitucion=restitucion)
        
    def eliminar_suelo(self):
        if self.suelo:
            self.suelo.eliminar()
            self.suelo = None
            
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
        self.gravedad = box2d.b2Vec2(x, y)
        #self.mundo = box2d.b2World(self.escenario, self.gravedad, True)
        print "Esta funcion esta en desuso..."


class Figura(object):
    "Representa un figura que simula un cuerpo fisico."

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

    def definir_velocidad_lineal(self, dx, dy):
        self._cuerpo.SetLinearVelocity((dx, dy))
        
    def eliminar(self):
        pilas.mundo.fisica.eliminar_figura(self._cuerpo)
        
    x = property(obtener_x, definir_x)
    y = property(obtener_y, definir_y)
    rotacion = property(obtener_rotacion, definir_rotacion)
    
class Circulo(Figura):
    "Representa un cuerpo de circulo."
    
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

class ConstanteDeDistancia():
    
    def __init__(self, figura_1, figura_2, fisica=None):
        if not fisica:
            fisica = pilas.mundo.fisica
            
        if not isinstance(figura_1, Figura) or not isinstance(figura_2, Figura):
            raise Exception("Las dos figuras tienen que ser objetos de la clase Figura.")
        
        constante = box2d.b2DistanceJointDef()
        constante.Initialize(c._cuerpo, c1._cuerpo, (0,0), (0,0))
        constante.collideConnected = True
        fisica.mundo.CreateJoint(constante)


def definir_gravedad(x=0, y=-90):
    pilas.mundo.fisica.mundo.gravity = (x, y)
