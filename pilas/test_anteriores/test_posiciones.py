import unittest
import pilas

class TestSequenceFunctions(unittest.TestCase):
    
    def testArea(self):
        caja = pilas.actores.Actor("caja.png")

        #  +------------+
        #  |            |
        #  |            |
        #  |      x     |
        #  |            |
        #  |            |
        #  +------------+

        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)

        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)

    def testEscalaReducida(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 0.5
        
        #  +------------+   # La caja resultado
        #  |            |   # es la interior.
        #  |   +----+   |
        #  |   |    |   |
        #  |   +----+   |
        #  |            |
        #  +------------+

    
        self.assertEqual(caja.alto, 24)
        self.assertEqual(caja.ancho, 24)

        self.assertEqual(caja.x, 0)
        self.assertEqual(caja.y, 0)

        self.assertEqual(caja.arriba, 12)
        self.assertEqual(caja.abajo, -12)
        self.assertEqual(caja.izquierda, -12)
        self.assertEqual(caja.derecha, 12)

    def testEscalaAmpliada(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 2

        self.assertEqual(caja.alto, 48*2)
        self.assertEqual(caja.ancho, 48*2)

        self.assertEqual(caja.x, 0)
        self.assertEqual(caja.y, 0)

        self.assertEqual(caja.arriba, 48)
        self.assertEqual(caja.abajo, -48)
        self.assertEqual(caja.izquierda, -48)
        self.assertEqual(caja.derecha, 48)
        
    def testCambioCentroHorizontal(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 1
        caja.centro = ("izquierda", "centro")
        #  +------------+
        #  |            |
        #  |            |
        #  |x           |
        #  |            |
        #  |            |
        #  +------------+
        
        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)

        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, 0)
        self.assertEqual(caja.derecha, 48)

        caja.centro = ("derecha", "centro")
        #  +------------+
        #  |            |
        #  |            |
        #  |           x|
        #  |            |
        #  |            |
        #  +------------+
        
        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, -48)
        self.assertEqual(caja.derecha, 0)

    def testCambioCentroVertical(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 1
        caja.centro = ("centro", "arriba")
        #  +------------+
        #  |      x     |
        #  |            |
        #  |            |
        #  |            |
        #  |            |
        #  +------------+
              
        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)
        
        self.assertEqual(caja.abajo, -48)
        self.assertEqual(caja.arriba, 0)

        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)

        caja.centro = ("centro", "abajo")
        #  +------------+
        #  |            |
        #  |            |
        #  |            |
        #  |            |
        #  |      x     |
        #  +------------+
        
        self.assertEqual(caja.arriba, 48)
        self.assertEqual(caja.abajo, 0)
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)
        
    def testCambioCentroVerticalYHorizontalNoCentrado(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 1
        
        caja.centro = (10, 10)
        
        #  +------------+
        #  |            |
        #  |   x        |
        #  |            |
        #  |            |
        #  |            |
        #  +------------+

        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)
        
        self.assertEqual(caja.abajo, -38)
        self.assertEqual(caja.arriba, 10)

        self.assertEqual(caja.izquierda, -10)
        self.assertEqual(caja.derecha, 38)

    def testCambioCentroVerticalYHorizontalNoCentradoConReduccionDeEscala(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 0.5
        
        caja.centro = (10, 10)
        
        #  +------------+
        #  |            |
        #  |   x        |
        #  |            |
        #  |            |
        #  |            |
        #  +------------+

        self.assertEqual(caja.alto, 24)
        self.assertEqual(caja.ancho, 24)
        
        self.assertEqual(caja.abajo, -38/2)
        self.assertEqual(caja.arriba, 5)

        self.assertEqual(caja.izquierda, -5)
        self.assertEqual(caja.derecha, 38/2)
        
    def testCambioDePosicionHorizontalConEscala(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 1
        
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)

        # Prueba dos cambios que no tendrian que afectar
        caja.izquierda = -24
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)
        
        caja.derecha = 24
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)
        
        caja.escala = 0.5
        
        self.assertEqual(caja.izquierda, -12)
        self.assertEqual(caja.derecha, 12)

        # Prueba dos cambios que no tendrian que afectar
        caja.izquierda = -20
        self.assertEqual(caja.izquierda, -20)
        self.assertEqual(caja.derecha, -20 + 24)
        
        caja.derecha = 0
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 0)        

    def testCambioDePosicionVerticalConEscala(self):
        caja = pilas.actores.Actor("caja.png")
        caja.centro = ("centro", "centro")
        caja.escala = 1
        
        self.assertEqual(caja.area, (48, 48))
        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)

        caja.arriba = 0
        self.assertEqual(caja.arriba, 0)
        self.assertEqual(caja.abajo, -48)
        
        caja.abajo = 0
        self.assertEqual(caja.arriba, 48)
        self.assertEqual(caja.abajo, 0)
        

        caja.escala = 0.5
        self.assertEqual(caja.area, (24, 24))
        caja.x, caja.y = (0, 0)

        self.assertEqual(caja.arriba, 12)
        self.assertEqual(caja.abajo, -12)

        # Prueba dos cambios que no tendrian que afectar
        caja.izquierda = -20
        self.assertEqual(caja.izquierda, -20)
        self.assertEqual(caja.derecha, -20 + 24)
        
        caja.derecha = 0
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 0)
        
        
pilas.iniciar()
unittest.main()


pilas.ejecutar()