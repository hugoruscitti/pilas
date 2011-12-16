import unittest
import pilas

class TestTerminar(unittest.TestCase):

    def setUp(self):
        pass

    def test_terminar(self):
        pilas.iniciar()
        pilas.terminar()

        pilas.iniciar()
        pilas.terminar()

if __name__ == '__main__':
    unittest.main()
