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

        mono.scale = 4
        self.assertEqual(mono.scale, 4)

        # Verifica que el personaje se pueda matar.
        mono.kill()
        self.assertFalse(mono in pilas.actors.all)



if __name__ == '__main__':
    unittest.main()
