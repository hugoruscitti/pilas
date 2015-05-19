# -*- encoding: utf-8 -*-
import sys
import time
import unittest

from PyQt4 import QtGui

import pilasengine


class TestActores(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
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

    class MiActor(pilasengine.actores.Actor):

        def iniciar(self):
            self.imagen = "aceituna.png"

        def actualizar(self):
            self.rotacion += 2

    class MiActorConArgumentos(pilasengine.actores.Actor):

        def iniciar(self, nombre, edad):
            self.imagen = "aceituna.png"
            self.nombre = nombre
            self.edad = edad

        def actualizar(self):
            self.rotacion += 2

    def setUp(self):
        self.pilas = pilasengine.iniciar()
        self.pilas.actores.vincular(TestActoresPersonalizados.MiActor)

    def testPuedeCrearActor(self):
        actor = self.pilas.actores.MiActor()
        self.assertTrue(actor, "Ha podido crear el objeto actor.")

    def testPuedeCrearActorConMetodoAlternativo(self):
        otro_actor = TestActoresPersonalizados.MiActor(self.pilas)
        self.assertTrue(otro_actor, "También funciona el método alternativo")

    def testPuedeVincularActorLuegoDeReiniciar(self):
        self.pilas.reiniciar()

        self.pilas.actores.vincular(TestActoresPersonalizados.MiActor)
        otro_actor = TestActoresPersonalizados.MiActor(self.pilas)
        self.assertTrue(otro_actor, "Puede volver a vincular un actor luego de \
                        reiniciar.")

    def testFallaCreacionActorSinArgumentos(self):
        def crear_actor_sin_argumentos():
            actor_falla = TestActoresPersonalizados.MiActor()

        self.assertRaises(Exception, crear_actor_sin_argumentos)

    def testFallaCreacionActorConArgumentosIncorrectos(self):
        def crear_actor_argumentos_incorrectos():
            actor_falla = TestActoresPersonalizados.MiActor(123)

        self.assertRaises(Exception, crear_actor_argumentos_incorrectos)

    def testFallaCreacionActorConArgumentosAdicionalesNoEsperados(self):
        def crear_actor_argumentos_adicionales_no_esperados():
            actor_falla = TestActoresPersonalizados.MiActor(self.pilas, 123)

        self.assertRaises(TypeError, crear_actor_argumentos_adicionales_no_esperados)

    def test_crear_actor_sin_los_argumentos_esperados(self):
        with self.assertRaises(TypeError):
            actor_falla = TestActoresPersonalizados.MiActorConArgumentos(self.pilas)

    def test_crear_actor_con_menos_argumentos_de_los_esperados(self):
        with self.assertRaises(TypeError):
            actor_falla = TestActoresPersonalizados.MiActorConArgumentos(self.pilas)

    def test_crear_actor_con_los_argumentos_correctos(self):
        actor = TestActoresPersonalizados.MiActorConArgumentos(self.pilas, nombre="pepe", edad=33)
        self.assertTrue(isinstance(actor, pilasengine.actores.Actor),
                        "Genera correctamente el actor usando argumentos.")

    def test_crear_actor_con_los_argumentos_correctos_como_diccionarios(self):
        actor = TestActoresPersonalizados.MiActorConArgumentos(self.pilas, edad=20, nombre="juan pepe")
        self.assertTrue(isinstance(actor, pilasengine.actores.Actor),
                        "Genera correctamente el actor usando argumentos como diccionario.")

    def test_crear_actor_con_mas_argumentos_de_los_esperados(self):
        with self.assertRaises(TypeError):
            actor = TestActoresPersonalizados.MiActorConArgumentos(self.pilas, pepe=123, otro=123, mas=222)


if __name__ == '__main__':
    unittest.main()
