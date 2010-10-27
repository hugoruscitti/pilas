# -*- encoding: utf-8 -*-
import random
import unittest
import pilas


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def testMundo(self):
        self.assertTrue(pilas.mundo)


    def testImage(self):
        original_image = pilas.imagenes.cargar('ceferino.png')

        actor = pilas.actores.Actor(original_image)
        actors_image = actor.GetImage()

        self.assertEqual(original_image, actors_image)

    def testScheduler(self):

        def none():
            pass

        def none_3(a, b, c):
            pass

        pilas.mundo.agregar_tarea(2, none)
        pilas.mundo.agregar_tarea(2, none_3, (1, 2, 3))

    def testInterpolation(self):
        a = pilas.interpolar([0, 100])
        self.assertEqual(a.values, [0, 100])

        # Invierte la interpolacion.
        a = -a
        self.assertEqual(a.values, [100, 0])

    def testText(self):
        texto = pilas.actores.Texto("Hola")
        self.assertEqual(texto.texto, "Hola")

        # verificando que el tamaño inicial es de 30 y el color negro
        self.assertEqual(texto.magnitud, 30)
        self.assertEqual(texto.color, (0, 0, 0, 255))

    def testComponents(self):
        texto = pilas.actores.Texto("Hola")

        # Vincula la clase Text con un componente.
        component = pilas.habilidades.AumentarConRueda 
        texto.aprender(component)
        
        # Se asegura que el componente pasa a ser de la superclase.
        superclases = texto.__class__.__bases__
        self.assertTrue(component in superclases)

    def testEjes(self):
        ejes = pilas.actores.Ejes()
        self.assertTrue(ejes)


    def testGrilla(self):
        grilla = pilas.imagenes.Grilla("volley.png", 10, 10)
        self.assertTrue(grilla)
        grilla.avanzar()

    def testFondo(self):
        grilla = pilas.escenas.Paisaje()


    def testControl(self):
        control = pilas.mundo.control

        self.assertFalse(control.izquierda)
        self.assertFalse(control.derecha)
        self.assertFalse(control.arriba)
        self.assertFalse(control.abajo)
        self.assertFalse(control.boton)

    def testDibujo(self):
        pizarra = pilas.actores.Pizarra()
        pizarra.dibujar_punto(20, 10)

    def testDistancias(self):
        self.assertEqual(0,  pilas.utils.distancia(0, 0))
        self.assertEqual(10, pilas.utils.distancia(0, 10))
        self.assertEqual(10, pilas.utils.distancia(0, -10))
        self.assertEqual(10, pilas.utils.distancia(-10, 0))

        self.assertEqual(0, pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 0)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((0, 0), (10, 0)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 10)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((10, 10), (0, 10)))

    def test_pieza_de_ejemplo(self):

        filas = 3
        columnas = 3

        grilla = pilas.imagenes.Grilla("ejemplos/data/piezas.png", filas, columnas)
        p = pilas.ejemplos.piezas.Pieza(None, grilla, 1, filas, columnas)

        self.assertEqual(p.numero, 1)
        self.assertEqual(p.numero_derecha, 2)
        self.assertEqual(p.numero_izquierda, 0)
        self.assertTrue(p.numero_arriba < 0)
        self.assertEqual(p.numero_abajo, 4)
        

        p = pilas.ejemplos.piezas.Pieza(None, grilla, 8, filas, columnas)

        self.assertEqual(p.numero, 8)
        self.assertEqual(p.numero_derecha, -1)   # la pieza 8 no tiene borde derecho.
        self.assertEqual(p.numero_izquierda, 7) 
        self.assertEqual(p.numero_arriba, 5)
        self.assertEqual(p.numero_abajo, 11) # la pieza 8 no tiene parte de abajo

    def test_posiciones_del_texto(self):
        m = pilas.actores.Texto("Hola")
        self.assertEquals(m.x, 0)

        ancho = m.obtener_ancho()
        algo = m.obtener_alto()

        # Verifica que la izquierda del actor esté asociada a la
        # posición 'x'.
        m.izquierda = m.izquierda - 50
        self.assertEquals(m.x, -50)

        m.izquierda = m.izquierda - 50
        self.assertEquals(m.x, -100)

        # Analiza si la parte derecha del actor esta vinculada a 'x'
        m.derecha = m.derecha + 50
        self.assertEquals(m.x, -50)

        # Verifica si la posicion superior e inferior alteran a 'y'
        self.assertEquals(m.y, 0)
        m.arriba = m.arriba - 100
        self.assertEquals(m.y, -100)

        m.abajo = m.abajo + 100
        self.assertEquals(m.y, 0)


    def test_posicion_y_magnitud(self):
        mono = pilas.actores.Mono()
        self.assertEqual(mono.x, 0)
        self.assertEqual(mono.y, 0)

        mono.izquierda = mono.izquierda - 100
        self.assertEqual(mono.x, -100)

        mono.derecha = mono.derecha + 100
        self.assertEqual(mono.x, 0)

        mono.arriba = mono.arriba + 100
        self.assertEquals(mono.y, 100)

        mono.abajo = mono.abajo - 100
        self.assertEquals(mono.y, 0)

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
