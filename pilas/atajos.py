# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas import dev

fabricar = pilas.actores.utils.fabricar


def crear_grupo(*k):
    """Genera un grupo."""
    return pilas.grupo.Grupo(k)


@dev.deprecated(se_desactiva_en="0.80", se_elimina_en="0.81",
                reemplazo="pilas.mundo.definir_gravedad")
def definir_gravedad(x, y):
    """Define la gravedad del motor de física.

    :param x: Aceleración horizontal.
    :param y: Aceleración vertical.
    """
    pilas.escena_actual().fisica.definir_gravedad(x, y)


def leer(texto, esperar = False):
    """Utiliza el comando speak para 'leer' un texto como sonido.

    :param texto: Cadena de texto a pronunciar.
    :param esperar: Si es True la función no vuelve hasta que se termina de leer el texo.
    :type esperar: boolean
    """
    try:
        from espeak import espeak
        import time
        espeak.set_voice('es-la')
        espeak.synth(texto)
        while esperar and espeak.is_playing():
            time.sleep(1)
    except ImportError:
        pass


def ocultar_puntero_del_mouse():
    """Oculta el puntero del mouse."""
    pilas.mundo.motor.ocultar_puntero_del_mouse()


def mostrar_puntero_del_mouse():
    """Muestra el puntero del mouse."""
    pilas.mundo.motor.mostrar_puntero_del_mouse()


def modo_pantalla_completa():
    """Pone Pilas a pantalla completa"""
    pilas.mundo.motor.ventana.canvas.pantalla_completa()


def modo_ventana():
    """Pone Pilas en modo ventana"""
    pilas.mundo.motor.ventana.canvas.pantalla_modo_ventana()


def definir_modos(*k, **kv):
    """Define los modos de depuración."""
    pilas.mundo.motor.canvas.depurador.definir_modos(*k, **kv)
