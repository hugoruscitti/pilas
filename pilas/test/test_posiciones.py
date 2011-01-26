import unittest
import pilas

class TestSequenceFunctions(unittest.TestCase):
    
    def testArea(self):
        caja = pilas.actores.Actor("caja.png")

        # En escala normal    
        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)

        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, -24)
        self.assertEqual(caja.derecha, 24)

    def testEscalaReducida(self):
        caja = pilas.actores.Actor("caja.png")
        caja.escala = 0.5
         
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
        
        self.assertEqual(caja.alto, 48)
        self.assertEqual(caja.ancho, 48)

        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, 0)
        self.assertEqual(caja.derecha, 48)

        caja.centro = ("derecha", "centro")
        self.assertEqual(caja.arriba, 24)
        self.assertEqual(caja.abajo, -24)
        self.assertEqual(caja.izquierda, -48)
        self.assertEqual(caja.derecha, 0)

pilas.iniciar()
unittest.main()


pilas.ejecutar()