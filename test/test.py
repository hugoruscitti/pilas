# -*- encoding: utf-8 -*-
import random
import unittest
import pilas

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_window_creation(self):
        self.assertFalse(pilas.app is None)

    def testVersion(self):
        pass

    def test_monkey_attributes(self):
        mono = pilas.actors.Monkey()

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.x = 100
        mono.y = 100

        self.assertEqual(mono.x, 100)
        self.assertEqual(mono.y, 100)

        # Se asegura que inicialmente no tenga rotacion asignada.
        self.assertEqual(mono.rotation, 0)

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.rotation = 180
        self.assertEqual(mono.rotation, 180)

        # Analiza que el personaje se ha agregado a la lista de actores.
        self.assertTrue(mono in pilas.actors.all)

        # Utiliza los atributos de escala.
        self.assertEqual(mono.scale, 1)
        mono.scale = 5
        self.assertEqual(mono.scale, 5)

        # Ejecuta mas metodos del mono.
        mono.smile()
        mono.shout()

        # Verifica que el personaje se pueda matar.
        mono.kill()
        self.assertFalse(mono in pilas.actors.all)

    def testImage(self):
        original_image = pilas.image.load('ceferino.png')

        actor = pilas.actors.Actor(original_image)
        actors_image = actor.GetImage()

        self.assertEqual(original_image, actors_image)

    def testScheduler(self):

        def none():
            pass

        def none_3(a, b, c):
            pass

        pilas.add_task(2, none)
        pilas.add_task(2, none_3, (1, 2, 3))

    def testInterpolation(self):
        a = pilas.interpolate(0, 100)
        self.assertEqual(a.values, (0, 100))

        # Invierte la interpolacion.
        a = -a
        self.assertEqual(a.values, (100, 0))

    def testText(self):
        texto = pilas.actors.Text("Hola")
        self.assertEqual(texto.text, "Hola")

        # verificando que el tamaño inicial es de 30 y el color negro
        self.assertEqual(texto.size, 30)
        self.assertEqual(texto.color, (0, 0, 0, 255))

    def testComponents(self):
        texto = pilas.actors.Text("Hola")

        # Vincula la clase Text con un componente.
        component = pilas.components.SizeByWheel 
        texto.mixin(component)
        
        # Se asegura que el componente pasa a ser de la superclase.
        superclases = texto.__class__.__bases__
        self.assertTrue(component in superclases)


if __name__ == '__main__':
    unittest.main()
