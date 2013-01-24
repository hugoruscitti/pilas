import unittest
import pilas

class TestEscenasYTareas(unittest.TestCase):

    def setUp(self):
        pilas.iniciar()

    def test_se_eliminan_las_tareas_al_cambiar_de_escena(self):

        una_tarea = pilas.mundo.agregar_tarea_siempre(0.5, self.funcion)
        self.assertEquals(pilas.mundo.tareas.obtener_cantidad_de_tareas_planificadas(), 1, "hay una tarea planificada.")

        class UnaEscena(pilas.escenas.Escena):
            pass

        class OtraEscena(pilas.escenas.Escena):
            pass


        UnaEscena()
        self.assertEquals(pilas.mundo.tareas.obtener_cantidad_de_tareas_planificadas(), 0, "se elimina correctamente la tarea planificada.")

        OtraEscena()
        self.assertEquals(pilas.mundo.tareas.obtener_cantidad_de_tareas_planificadas(), 0, "se elimina correctamente la tarea planificada.")

    def funcion(self):
        pass

if __name__ == '__main__':
    unittest.main()
