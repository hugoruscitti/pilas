# -*- encoding: utf-8 -*-
import sys
import unittest
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtTest import QTest

import pilasengine


class TestControles(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

    def testRealizaMovimientoConControles(self):

        class ActorConControles(pilasengine.actores.actor.Actor):

            def actualizar(self):
                control = self.pilas.escena_actual().control

                if control.derecha:
                    self.x += 1
                elif control.izquierda:
                    self.x -= 1

        actor = ActorConControles(self.pilas)
        self.assertEqual(0, actor.x, "Comienza en el punto (0, 0)")

        # Simula la pulsación de la tecla Derecha
        widget = self.pilas.obtener_widget()
        QTest.keyPress(widget, QtCore.Qt.Key_Right)

        # Simula que pasó un solo tick (si hago 60 de estos simulará 1 segundo).
        self.pilas.simular_actualizacion_logica()

        self.assertEqual(1, actor.x, "Luego de pulsar DERECHA se mueve")

        # importante: suelta la tecla que comezó a pulsar antes.
        QTest.keyRelease(widget, QtCore.Qt.Key_Right)

        # Pulsa dos veces hacia la izquierda:
        QTest.keyPress(widget, QtCore.Qt.Key_Left)
        self.pilas.simular_actualizacion_logica()
        QTest.keyPress(widget, QtCore.Qt.Key_Left)
        self.pilas.simular_actualizacion_logica()

        self.assertEqual(-1, actor.x, "Luego de pulsar dos veces \
                         IZQUIERDA pasa a x=-1")


if __name__ == '__main__':
    unittest.main()