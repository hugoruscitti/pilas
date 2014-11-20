# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui
import pilasengine


class TestActores(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearActores(self):
        actor = self.pilas.actores.Aceituna()
        self.assertTrue(actor, "Puede crear un actor.")

        actor = self.pilas.actores.Texto()
        self.assertTrue(actor, "Puede crear un actor texto.")

    def testFuncionanInterpolacionesSimples(self):
        actor = self.pilas.actores.Aceituna()
        self.assertEquals(0, actor.x, "Está en la posición inicial")

        actor.x = [100]

        self.assertEquals(0, actor.x, "Está en la posición inicial")
        escena = self.pilas.obtener_escena_actual()
        escena.actualizar_interpolaciones()
        self.assertTrue(actor.x > 0, "El actor se mueve un poco a la derecha")

        # Simula el paso de un segundo
        import time
        time.sleep(0.5)

        escena.actualizar_interpolaciones()
        self.assertTrue(actor.x == 100, actor.x)

    def testPuedeCrearActorPersonalizado(self):
        class MiActor(pilasengine.actores.Actor):

            def iniciar(self):
                self.imagen = "aceituna.png"

            def actualizar(self):
                self.rotacion += 2

        self.pilas.actores.vincular(MiActor)
        actor = self.pilas.actores.MiActor()
        self.assertTrue(actor, "Ha podido crear el objeto actor.")

        otro_actor = MiActor(self.pilas)
        self.assertTrue(otro_actor, "También funciona el método alternativo")

        self.pilas.reiniciar()

        self.pilas.actores.vincular(MiActor)
        otro_actor = MiActor(self.pilas)
        self.assertTrue(otro_actor, "Puede volver a vincular un actor luego de \
                        reiniciar.")

        def crear_actor_sin_argumentos():
            actor_falla = MiActor()

        self.assertRaises(Exception, crear_actor_sin_argumentos)

        def crear_actor_argumentos_incorrectos():
            actor_falla = MiActor(123)

        self.assertRaises(Exception, crear_actor_argumentos_incorrectos)

    def testObtieneErrorSiElActorPersonalizadoExiste(self):
        class Actor(pilasengine.actores.Actor):

            def iniciar(self):
                self.imagen = "aceituna.png"

            def actualizar(self):
                self.rotacion += 2

        def crear_actor_que_existe():
            self.pilas.actores.vincular(Actor)

        self.assertRaises(Exception, crear_actor_que_existe)

    def testRealizaMovimientoConInterpolacion(self):
        aceituna = self.pilas.actores.Aceituna()

        self.assertEqual(0, aceituna.x, "Comienza en el punto (0, 0)")
        aceituna.x = [100], 1

        # Simula que pasaron 60 ticks (osea 1 segundo).
        for x in range(60):
            self.pilas.simular_actualizacion_logica()

        self.assertEqual(100.0, aceituna.x, "Luego de 60 ticks (1 segundo) \
                         llegó a x=100")


    def testPuedeInstanciarTodosLosActoresSinArgumentos(self):
        nombres = [n for n in dir(self.pilas.actores) if n.istitle()]
        funciones = [getattr(self.pilas.actores, n) for n in nombres]

        for x in funciones:
            actor = x()
            self.assertTrue(actor, "Puede crear el actor %s" %(str(x)))

if __name__ == '__main__':
    unittest.main()
