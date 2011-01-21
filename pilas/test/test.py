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
        actors_image = actor.imagen

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

    def testComponents(self):
        texto = pilas.actores.Texto("Hola")

        # Vincula la clase Text con un componente.
        component = pilas.habilidades.AumentarConRueda 
        texto.aprender(component)

        # Se asegura que el componente pasa a ser de la superclase.
        self.assertTrue(component == texto.habilidades[0].__class__)

    def testAtajos(self):
        pilas.atajos

    def testEjes(self):
        ejes = pilas.actores.Ejes()
        self.assertTrue(ejes)


    def testGrilla(self):
        grilla = pilas.imagenes.cargar_grilla("fondos/volley.png", 10, 10)
        self.assertTrue(grilla)
        grilla.avanzar()

    def testFondo(self):
        grilla = pilas.fondos.Tarde()
        self.assertTrue(grilla)


    def testControl(self):
        control = pilas.mundo.control

        self.assertFalse(control.izquierda)
        self.assertFalse(control.derecha)
        self.assertFalse(control.arriba)
        self.assertFalse(control.abajo)
        self.assertFalse(control.boton)


    def testDistancias(self):
        self.assertEqual(0,  pilas.utils.distancia(0, 0))
        self.assertEqual(10, pilas.utils.distancia(0, 10))
        self.assertEqual(10, pilas.utils.distancia(0, -10))
        self.assertEqual(10, pilas.utils.distancia(-10, 0))

        self.assertEqual(0, pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 0)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((0, 0), (10, 0)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 10)))
        self.assertEqual(10, pilas.utils.distancia_entre_dos_puntos((10, 10), (0, 10)))


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

    def test_ver_codigo(self):
        pilas.ver(pilas)


if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
