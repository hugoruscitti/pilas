# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from PyQt4 import QtCore

from pilasengine.controles import simbolos
from pilasengine.controles import control

TECLAS = {
    QtCore.Qt.Key_Left: simbolos.IZQUIERDA,
    QtCore.Qt.Key_Right: simbolos.DERECHA,
    QtCore.Qt.Key_Up: simbolos.ARRIBA,
    QtCore.Qt.Key_Down: simbolos.ABAJO,
    QtCore.Qt.Key_Space: simbolos.ESPACIO,
    QtCore.Qt.Key_Return: simbolos.SELECCION,
    QtCore.Qt.Key_Shift: simbolos.SHIFT,
    QtCore.Qt.Key_Control: simbolos.CTRL,
    QtCore.Qt.Key_AltGr: simbolos.ALTGR,
    QtCore.Qt.Key_Alt: simbolos.ALT,
    QtCore.Qt.Key_CapsLock: simbolos.CAPSLOCK,
    QtCore.Qt.Key_F1: simbolos.F1,
    QtCore.Qt.Key_F2: simbolos.F2,
    QtCore.Qt.Key_F3: simbolos.F3,
    QtCore.Qt.Key_F4: simbolos.F4,
    QtCore.Qt.Key_F5: simbolos.F5,
    QtCore.Qt.Key_F6: simbolos.F6,
    QtCore.Qt.Key_F7: simbolos.F7,
    QtCore.Qt.Key_F8: simbolos.F8,
    QtCore.Qt.Key_F9: simbolos.F9,
    QtCore.Qt.Key_F10: simbolos.F10,
    QtCore.Qt.Key_F11: simbolos.F11,
    QtCore.Qt.Key_F12: simbolos.F12,
    QtCore.Qt.Key_A: simbolos.a,
    QtCore.Qt.Key_B: simbolos.b,
    QtCore.Qt.Key_C: simbolos.c,
    QtCore.Qt.Key_D: simbolos.d,
    QtCore.Qt.Key_E: simbolos.e,
    QtCore.Qt.Key_F: simbolos.f,
    QtCore.Qt.Key_G: simbolos.g,
    QtCore.Qt.Key_H: simbolos.h,
    QtCore.Qt.Key_I: simbolos.i,
    QtCore.Qt.Key_J: simbolos.j,
    QtCore.Qt.Key_K: simbolos.k,
    QtCore.Qt.Key_L: simbolos.l,
    QtCore.Qt.Key_M: simbolos.m,
    QtCore.Qt.Key_N: simbolos.n,
    QtCore.Qt.Key_O: simbolos.o,
    QtCore.Qt.Key_P: simbolos.p,
    QtCore.Qt.Key_Q: simbolos.q,
    QtCore.Qt.Key_R: simbolos.r,
    QtCore.Qt.Key_S: simbolos.s,
    QtCore.Qt.Key_T: simbolos.t,
    QtCore.Qt.Key_U: simbolos.u,
    QtCore.Qt.Key_V: simbolos.v,
    QtCore.Qt.Key_W: simbolos.w,
    QtCore.Qt.Key_X: simbolos.x,
    QtCore.Qt.Key_Y: simbolos.y,
    QtCore.Qt.Key_Z: simbolos.z,
}


class Controles(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def Control(self, escena, mapa_teclado=None):
        return control.Control(escena, mapa_teclado)

    @staticmethod
    def obtener_codigo_de_tecla_normalizado(tecla_qt):
        return TECLAS.get(tecla_qt, tecla_qt)