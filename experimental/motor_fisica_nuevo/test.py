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