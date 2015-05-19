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
        nombres = [n for n in dir(self.pilas.actores) if n.istitle() and n is not 'Grupo']
        funciones = [getattr(self.pilas.actores, n) for n in nombres]

        for x in funciones:
            actor = x()
            self.assertTrue(actor, "Puede crear el actor %s" %(str(x)))

    def testFuncionaHerenciaDeActoresYaExistentes(self):

        class ActorHeredado(pilasengine.actores.Mono):
            pass

        b = ActorHeredado(self.pilas)
        self.assertTrue(b.imagen, "Hereda correctamente")

        class ActorAceituna(pilasengine.actores.Aceituna):
            pass

        b = ActorAceituna(self.pilas)
        self.assertTrue(b.imagen, "Hereda correctamente")

    def testEtiquetas(self):

        # Se asegura que todos los actores nacen con
        # una etiqueta que identifica la clase.

        m = self.pilas.actores.Mono()
        self.assertEquals(str(m.etiquetas), "['mono']")

        a = self.pilas.actores.Aceituna()
        self.assertEquals(str(a.etiquetas), "['aceituna']")

        # Se asegura que se pueden agregar y eliminar
        # etiquetas

        a.etiquetas.agregar('enemigo')
        self.assertEquals(str(a.etiquetas), "['aceituna', 'enemigo']")

        a.etiquetas.eliminar('enemigo')
        self.assertEquals(str(a.etiquetas), "['aceituna']")


class TestActoresPersonalizados(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

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

        def crear_actor_argumentos_adicionales_no_esperados():
            actor_falla = MiActor(self.pilas, 123)

        self.assertRaises(TypeError, crear_actor_argumentos_adicionales_no_esperados)

        class MiActorConArgumentos(pilasengine.actores.Actor):

            def iniciar(self, nombre, edad):
                self.imagen = "aceituna.png"
                self.nombre = nombre
                self.edad = edad


            def actualizar(self):
                self.rotacion += 2

        def crear_actor_sin_los_argumentos_esperados():
            actor_falla = MiActorConArgumentos(self.pilas)

        def crear_actor_con_menos_argumentos_de_los_esperados():
            actor_falla = MiActorConArgumentos(self.pilas)

        def crear_actor_con_los_argumentos_correctos():
            actor = MiActorConArgumentos(self.pilas, nombre="pepe", edad=33)
            return actor

        def crear_actor_con_los_argumentos_correctos_como_diccionarios():
            actor = MiActorConArgumentos(self.pilas, edad=20, nombre="juan pepe")
            return actor

        def crear_actor_con_mas_argumentos_de_los_esperados():
            actor = MiActorConArgumentos(self.pilas, pepe=123, otro=123, mas=222)
            return actor

        # Prueba que falle crear actores con argumentos faltantes.
        self.assertRaises(TypeError, crear_actor_sin_los_argumentos_esperados)
        self.assertRaises(TypeError, crear_actor_con_menos_argumentos_de_los_esperados)
        self.assertRaises(TypeError, crear_actor_con_mas_argumentos_de_los_esperados)


        # Se asegura de crear los actores correctamente y ver que funcionan.
        self.assertTrue(isinstance(crear_actor_con_los_argumentos_correctos(), pilasengine.actores.Actor), "Genera correctamente el actor usando argumentos.")
        self.assertTrue(isinstance(crear_actor_con_los_argumentos_correctos_como_diccionarios(), pilasengine.actores.Actor), "Genera correctamente el actor usando argumentos como diccionario.")


if __name__ == '__main__':
    unittest.main()
