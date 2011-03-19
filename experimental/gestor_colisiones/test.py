import pilas
import Box2D as box2d

pilas.iniciar()

c1 = pilas.actores.Caja(y=100)
c2 = pilas.actores.Caja()

# FIXME: Esto no tiene que estar afuera, sino integrado
#        dentro el motor, porque en realidad uno solamente
#        suele querer re-definir las funcione add, remove y persist.
class myContactListener(box2d.b2ContactListener):
    def __init__(self):
        box2d.b2ContactListener.__init__(self)

    def Add(self, point):
        figura_1 = point.shape1
        figura_2 = point.shape2
        posicion = point.position.copy()
        #cp.normal   = point.normal.copy()
        #cp.id       = point.id
        pilas.actores.Explosion(posicion.x, posicion.y)

    def Remove(self, point):
        'Termina la colision entre dos puntos'
        pass

    def Persist(self, punto):
        "Se queda quieto..."
        pass

a = myContactListener()
pilas.mundo.fisica.mundo.SetContactListener(a)

pilas.avisar("Creando colisiones en los puntos de contacto.")
pilas.ejecutar()
