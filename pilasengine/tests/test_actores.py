# -*- encoding: utf-8 -*-
import sys
import time
import unittest

from PyQt4 import QtGui

import pilasengine

class SubTexto(pilasengine.actores.Texto):
    def iniciar(self):
        self.texto = "hola"


class TestActores(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar(modo_test=True)

    def testPuedeCrearActores(self):
        actor = self.pilas.actores.Aceituna()
        self.assertTrue(actor, "Puede crear un actor.")

        actor = self.pilas.actores.Texto()
        self.assertTrue(actor, "Puede crear un actor texto.")
        self.assertTrue(actor.texto, "Sin texto")

        actor = SubTexto(self.pilas)
        self.assertTrue(actor, "Puede crear un actor sub-texto.")
        self.assertTrue(actor.texto, "hola")

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

        with self.assertRaises(Exception):
            self.pilas.actores.vincular(Actor)

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
        self.assertTrue(nombres, "No se encontraron actores para testear")

        funciones = [getattr(self.pilas.actores, n) for n in nombres]

        for x in funciones:
            actor = x()
            self.assertTrue(actor, "Puede crear el actor %s" %(str(x)))

    def testFuncionaHerenciaDeActoresYaExistentes(self):

        class ActorHeredado(pilasengine.actores.Mono):
            pass

        heredado_de_mono = ActorHeredado(self.pilas)
        self.assertTrue(heredado_de_mono.imagen, "Hereda correctamente")

        class ActorAceituna(pilasengine.actores.Aceituna):
            pass

        heredado_de_aceituna = ActorAceituna(self.pilas)
        self.assertTrue(heredado_de_aceituna.imagen, "Hereda correctamente")

    def test_el_actor_esta_visible(self):
        actor = self.pilas.actores.Aceituna()
        self.assertFalse(actor.esta_fuera_de_la_pantalla(), "El actor inicialmente esta dentro de la pantalla")

        actor.x = 600
        self.assertTrue(actor.esta_fuera_de_la_pantalla(), "Luego de moverse 600 pixeles ya no se ve")

        self.pilas.camara.x = 600
        self.assertFalse(actor.esta_fuera_de_la_pantalla(), "Si la camara lo apunta lo vemos de nuevo")

        self.pilas.camara.x = 0
        self.pilas.camara.escala = 0.5
        self.assertFalse(actor.esta_fuera_de_la_pantalla(), "Si la camara regresa a 0, pero tiene poco zoom tambien se ve.")


        self.assertTrue(actor.esta_dentro_de_la_pantalla(), "y el metodo esta_dentro_de_la_pantalla retorna lo contrario")

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
        self.pilas = pilasengine.iniciar(modo_test=True)
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

    def test_listar_clases_de_actores(self):
        clases = self.pilas.actores.obtener_clases()

        self.assertTrue('Misil' in clases, "Existe la clase Misil")
        self.assertTrue('Actor' in clases, "Existe la clase Actor")
        self.assertTrue('Aceituna' in clases, "Existe la clase Aceituna")



if __name__ == '__main__':
    unittest.main()
