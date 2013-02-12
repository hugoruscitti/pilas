import unittest
import pilas

class TestEscenasYTareas(unittest.TestCase):

    def setUp(self):
        pilas.iniciar()

    def test_se_eliminan_las_tareas_al_cambiar_de_escena(self):

        una_tarea = pilas.mundo.agregar_tarea_siempre(0.5, self.funcion)
        self.assertEquals(pilas.escena_actual().tareas.obtener_cantidad_de_tareas_planificadas(),
                          1, "hay una tarea planificada.")

        class UnaEscena(pilas.escena.Normal):
            pass

        class OtraEscena(pilas.escena.Normal):
            pass


        pilas.cambiar_escena(UnaEscena())
        self.assertEquals(pilas.escena_actual().tareas.obtener_cantidad_de_tareas_planificadas(), 0,
                          "se elimina correctamente la tarea planificada.")


    def funcion(self):
        pass

if __name__ == '__main__':
    unittest.main()
