import pilas
import Box2D as box2d
import math

# Este ejemplo muestra un motor de fisica que
# usa box2d pero no necesita de elements. Tambien
# usa el objeto pizarra, que lo hace mas adecuado
# para integrar a pilas.

# Si las pruebas salen bien, me gustaria reemplazar
# a elements por estos objetos, principalmente porque
# creo que la visualizacion de la pizarra puede
# estar deshabilitada, y que se pueda habitar con
# una tecla. De esa forma el motor de fisica puede
# ser una simulacion invisible, y que se puede
# ver con fines de depuracion.




class Fisica(object):
    "Representa un simulador de mundo fisico, usando la biblioteca box2d."
    
    def __init__(self):
        self.escenario = box2d.b2AABB()
        self.escenario.lowerBound = (-1000.0, -1000.0)
        self.escenario.upperBound = (1000.0, 1000.0)
        
        self.mundo = box2d.b2World(self.escenario, (0.0, -90.0), True)
        
        self.pizarra = pilas.actores.Pizarra()
        self.pizarra.deshabilitar_actualizacion_automatica()
        self.i = 0

    def actualizar(self):
        self.mundo.Step(1.0 / 20.0, 10, 8)
        self.i += 1
        
        if self.i % 2  == 0:
            self.dibujar_figuras()
        
    def dibujar_figuras(self):
        "Dibuja todas las figuras en una pizarra. Indicado para depuracion."
        cuerpos = self.mundo.bodyList
        cantidad_de_figuras = 0
        
        self.pizarra.limpiar()
        
        self.pizarra.definir_color(pilas.colores.negro)
        self.pizarra.canvas.context.set_antialias(False)
        
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
                        
                    self.pizarra.dibujar_poligono(vertices)
                    
                elif tipo_de_figura == box2d.e_circleShape:
                    self.pizarra.dibujar_circulo(cuerpo.position.x, cuerpo.position.y, figura.radius, False)
                else:
                    print "no se que este esta figura..."

        self.pizarra.actualizar_imagen()
        
    def crear_cuerpo(self, definicion_de_cuerpo):
        return self.mundo.CreateBody(definicion_de_cuerpo)

    def crear_suelo(self):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(0.0, -240)

        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        dynamic = False
        # Create the Body
        if not dynamic:
            density = 0

        body = self.mundo.CreateBody(bodyDef)
                    
        #self.parent.element_count += 1

        # Add a shape to the Body
        boxDef = box2d.b2PolygonDef()
        
        width = 640
        height= 1
        boxDef.SetAsBox(width, height, (0,0), 0)
        

        restitution=0.16
        friction=0.5
        
        boxDef.density = density
        boxDef.restitution = restitution
        boxDef.friction = friction
        body.CreateShape(boxDef)
        
        body.SetMassFromShapes()
    
        self.suelo = body
        
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

    x = property(obtener_x, definir_x)
    y = property(obtener_y, definir_y)
    rotacion = property(obtener_rotacion, definir_rotacion)
    
class Circulo(Figura):
    "Representa un cuerpo de circulo."
    
    def __init__(self, fisica, x, y, radio, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

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
    
    def __init__(self, fisica, x, y, ancho, alto, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        #self.parent.element_count += 1
        
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        # Add a shape to the Body
        boxDef = box2d.b2PolygonDef()
        
        boxDef.SetAsBox(ancho, alto, (0,0), 0)
        boxDef.density = densidad
        boxDef.restitution = restitucion
        boxDef.friction = friccion
        body.CreateShape(boxDef)

        body.SetMassFromShapes()    

        self._cuerpo = body

class ConstanteDeDistancia():
    
    def __init__(self, figura_1, figura_2):
        if not isinstance(figura_1, Figura) or not isinstance(figura_2, Figura):
            raise Exception("Las dos figuras tienen que ser objetos de la clase Figura.")
        
        constante = box2d.b2DistanceJointDef()
        constante.Initialize(c._cuerpo, c1._cuerpo, (0,0), (0,0))
        constante.collideConnected = True
        f.mundo.CreateJoint(constante)

        
class Actor(pilas.actores.Actor):
    
    def __init__(self, figura_a_imitar):
        self.figura_a_imitar = figura_a_imitar
        pilas.actores.Actor.__init__(self, "pelota.png")

    def actualizar(self):
        self.x = self.figura_a_imitar.x
        self.y = self.figura_a_imitar.y
        self.rotacion = self.figura_a_imitar.rotacion
        
    def tiene_figura(self):
        return self.figura_a_imitar
        
class Caja(Actor):
    
    def __init__(self, figura_a_imitar):
        pilas.actores.Actor.__init__(self, "caja.png")
        self.figura_a_imitar = figura_a_imitar

class Jugador(pilas.actores.Actor):
    
    def __init__(self):
        pilas.actores.Actor.__init__(self, "protagonista.png")
        self.dy = 0
        self.y = 100
        self.centro = ("centro", 110)
        self.en_el_aire = True
        
    def actualizar(self):
        c = pilas.mundo.control
        
        if c.izquierda:
            self.x -= 5
            self.espejado = True
        if c.derecha:
            self.x += 5
            self.espejado = False
        
        if self.en_el_aire:
            self.dy += 0.5
        
            if self.dy > 0:
                delta = f.obtener_distancia_al_suelo(self.x, self.y, self.dy)
                
                
                if delta < self.dy:
                    self.y -= delta
                    self.en_el_aire = False
                    self.dy = 0
                    
                #if delta > 2:
                #    self.dy = 0
                #    self.en_el_aire = False
                #    print "Toca el suelo a la distancia:", delta
        else:
            if c.arriba:
                self.dy = -10           
                self.en_el_aire = True
                
            distancia_al_suelo = f.obtener_distancia_al_suelo(self.x, self.y - 5, 10)
            
            if distancia_al_suelo == 10:
                self.en_el_aire = True
            else:
                self.y -= distancia_al_suelo - 1
            
            
        self.y -= self.dy
        
        

pilas.iniciar() 

# INICIO: Luego tiene que estar dentro del modulo pilas.
f = Fisica()
f.crear_suelo()

def actualizar_motor(evento):
    f.actualizar()

pilas.eventos.actualizar.conectar(actualizar_motor)
# FIN: -----------

radio = 25


def click(evento):
    x = evento.x
    y = evento.y
    
    if evento.button == 0:
        c = Circulo(f, x, y, radio=25)
        actor = Actor(c)
    else:
        c = Rectangulo(f, x, y, ancho=25, alto=25)
        actor = Caja(c)



class ImpulsadoPorTeclado(pilas.habilidades.Habilidad):
    
    def __init__(self, receptor):
        if not receptor.tiene_figura():
            raise Exception("No puede asignar esta habilidad a un actor sin figura fisica.")
        
        self.receptor = receptor

    def actualizar(self):
        c = pilas.mundo.control
        velocidad = 10
        
        if c.izquierda:
            self.receptor.figura_a_imitar.x -= velocidad
        elif c.derecha:
            self.receptor.figura_a_imitar.x += velocidad
            
        if c.arriba:
            self.receptor.figura_a_imitar.y += 50

# Interface


def crear_objetos_con_clicks():
    pilas.eventos.click_de_mouse.conectar(click)
    pilas.avisar("Pulsa los botones izquierdo o derecho del mouse para crear figuras.")

def crear_dos_objetos_con_distancia_fija():
    # El argumento 'f' (fisica) se tendria que eliminar y ser implicito.

    c = Circulo(f, 0, 0, radio)
    actor = Actor(c)
    
    c1 = Circulo(f, 10, 200, radio)
    actor2 = Actor(c1)
    
    # aplica distancia entre las dos pelotas.
    distancia = ConstanteDeDistancia(c, c1)

def mover_objeto_con_el_teclado():
    c = Circulo(f, 0, 200, radio)
    actor = Actor(c)
    actor.aprender(ImpulsadoPorTeclado)

def obtener_distancia_al_suelo():
    
    def imprimir_posicion(evento):
        x, y = evento.x, evento.y
        
        print f.obtener_distancia_al_suelo(x, y, 200)
        
    pilas.eventos.click_de_mouse.conectar(imprimir_posicion)


def juego_de_plataformas():
    c = Rectangulo(f, 0, 0, dinamica=False, ancho=25, alto=25)
    actor = Caja(c)
    
    c = Rectangulo(f, 100, 0, dinamica=False, ancho=25, alto=25)
    actor = Caja(c)
    
    c = Rectangulo(f, -100, 0, dinamica=False, ancho=25, alto=25)
    actor = Caja(c)
    
    c = Rectangulo(f, -190, -100, dinamica=False, ancho=25, alto=25)
    actor = Caja(c)

    c = Rectangulo(f, -100, -200, dinamica=False, ancho=25, alto=25)
    actor = Caja(c)

    Jugador()

juego_de_plataformas()
crear_objetos_con_clicks()

pilas.ejecutar()