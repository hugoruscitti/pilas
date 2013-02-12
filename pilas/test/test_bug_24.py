import unittest
import pilas

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pilas.iniciar()
        self.eactual = pilas.escena_actual()
        for t in list(self.eactual.tareas.tareas_planificadas):
            t.terminar()

    def test_shuffle(self):
        una_tarea = pilas.mundo.agregar_tarea_siempre(0.5, self.funcion)
        self.assertEquals(self.eactual.tareas.obtener_cantidad_de_tareas_planificadas(),
                          1, "hay una tarea planificada.")

        una_tarea.terminar()
        self.assertEquals(self.eactual.tareas.obtener_cantidad_de_tareas_planificadas(),
                          0, "se elimina correctamente la tarea planificada.")

    def funcion(self):
        pass

if __name__ == '__main__':
    unittest.main()
