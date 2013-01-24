import unittest
import pilas

class TestEscenasYTareas(unittest.TestCase):

    def setUp(self):
        pilas.iniciar()

    def test_las_habilidades_no_se_actualizan_antes_de_inicializar(self):
        un_actor = pilas.actores.Actor()
        un_comportamiento = pilas.comportamientos.Girar(20, 30)
        un_actor.hacer(un_comportamiento)

        pingu = pilas.actores.Pingu()
        pingu.actualizar()

if __name__ == '__main__':
    unittest.main()
