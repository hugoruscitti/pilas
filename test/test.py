# -*- encoding: utf-8 -*-
import random
import unittest
import pilas


class TestSequenceFunctions(unittest.TestCase):
    

    def setUp(self):
        pass

    def testMundo(self):
        self.assertTrue(pilas.mundo)

    def test_monkey_attributes(self):
        mono = pilas.actores.Mono()

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.x = 100
        mono.y = 100

        self.assertEqual(mono.x, 100)
        self.assertEqual(mono.y, 100)

        # Se asegura que inicialmente no tenga rotacion asignada.
        self.assertEqual(mono.rotacion, 0)

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.rotacion = 180
        self.assertEqual(mono.rotacion, 180)

        mono.rotacion = 20
        self.assertEqual(mono.rotacion, 20)

        mono.rotacion = 400
        self.assertEqual(mono.rotacion, (400 % 360))

        # Analiza que el personaje se ha agregado a la lista de actores.
        self.assertTrue(mono in pilas.actores.todos)

        # Utiliza los atributos de escala.
        self.assertEqual(mono.escala, 1)
        mono.escala = 5
        self.assertEqual(mono.escala, 5)

        # Ejecuta mas metodos del mono.
        mono.sonreir()
        mono.gritar()

        # Verifica que el personaje se pueda matar.
        mono.eliminar()
        self.assertFalse(mono in pilas.actores.todos)

    def testImage(self):
        original_image = pilas.imagenes.cargar('ceferino.png')

        actor = pilas.actores.Actor(original_image)
        actors_image = actor.GetImage()

        self.assertEqual(original_image, actors_image)

    def testScheduler(self):

        def none():
            pass

        def none_3(a, b, c):
            pass

        pilas.agregar_tarea(2, none)
        pilas.agregar_tarea(2, none_3, (1, 2, 3))

    def testInterpolation(self):
        a = pilas.interpolar(0, 100)
        self.assertEqual(a.values, (0, 100))

        # Invierte la interpolacion.
        a = -a
        self.assertEqual(a.values, (100, 0))

    def testText(self):
        texto = pilas.actores.Texto("Hola")
        self.assertEqual(texto.texto, "Hola")

        # verificando que el tamaño inicial es de 30 y el color negro
        self.assertEqual(texto.magnitud, 30)
        self.assertEqual(texto.color, (0, 0, 0, 255))

    def testComponents(self):
        texto = pilas.actores.Texto("Hola")

        # Vincula la clase Text con un componente.
        component = pilas.habilidades.AumentarConRueda 
        texto.aprender(component)
        
        # Se asegura que el componente pasa a ser de la superclase.
        superclases = texto.__class__.__bases__
        self.assertTrue(component in superclases)

    def testEjes(self):
        ejes = pilas.actores.Ejes()
        self.assertTrue(ejes)

    def testDepuracion(self):
        pilas.ventana.alternar_modo_depuracion()

    def testGrilla(self):
        grilla = pilas.imagenes.Grilla("volley.png", 10, 10)
        self.assertTrue(grilla)
        grilla.avanzar()

    def testFondo(self):
        grilla = pilas.escenas.Paisaje()


    def testControl(self):
        control = pilas.mundo.control

        self.assertFalse(control.izquierda)
        self.assertFalse(control.derecha)
        self.assertFalse(control.arriba)
        self.assertFalse(control.abajo)
        self.assertFalse(control.boton)

    def testDibujo(self):
        pizarra = pilas.actores.Pizarra()
        pizarra.dibujar_punto(20, 10)

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
