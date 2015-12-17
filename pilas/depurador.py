# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import sys
import pilas
from pilas import pilasversion

try:
    from . import widget_log
except ImportError as e:
    print(e)
    pass

class DepuradorDeshabilitado(object):

    def comienza_dibujado(self, motor, painter):
        pass

    def dibuja_al_actor(self, motor, painter, actor):
        pass

    def termina_dibujado(self, motor, painter):
        pass

    def cuando_pulsa_tecla(self, codigo_tecla, texto_tecla):
        pass

    def cuando_mueve_el_mouse(self, x, y):
        pass

    def reiniciar(self):
        pass

class Depurador(DepuradorDeshabilitado):
    """Esta clase permite hacer depuraciones visuales.

    La depuracion visual en pilas consiste en poder mostrar informacion
    que generalmente es invisible a los jugadores. Por ejemplo, donde
    estan situados los puntos de control, los radios de colision etc.

    Esta clase administra varios modos depuracion, que son los
    que dibujan figuras geometricas.
    """

    def __init__(self, lienzo, fps):
        self.modos = []
        self.lienzo = lienzo
        ModoDepurador.grosor_de_lineas = 4
        self.fps = fps
        self.posicion_del_mouse = (0, 0)

    def comienza_dibujado(self, motor, painter):
        for m in self.modos:
            m.comienza_dibujado(motor, painter, self.lienzo)

    def dibuja_al_actor(self, motor, painter, actor):
        for m in self.modos:
            m.dibuja_al_actor(motor, painter, self.lienzo, actor)

    def termina_dibujado(self, motor, painter):
        if self.modos:
            self._mostrar_cantidad_de_cuerpos(painter)
            self._mostrar_cantidad_de_actores(painter)
            self._mostrar_cuadros_por_segundo(painter)
            self._mostrar_posicion_del_mouse(painter)
            self._mostrar_nombres_de_modos(painter)
            self._mostrar_cantidad_de_imagenes_cacheadas(painter)

            for m in self.modos:
                m.termina_dibujado(motor, painter, self.lienzo)

    def cuando_pulsa_tecla(self, codigo_tecla, texto_tecla):
        if codigo_tecla == 'F2':
            pilas.mundo.motor.capturar_pantalla("captura_pantalla.png")
        elif codigo_tecla == 'F5':
            self._alternar_modo(ModoWidgetLog)
        elif codigo_tecla == 'F6':
            pilas.utils.imprimir_todos_los_eventos()
        elif codigo_tecla == 'F7':
            self._alternar_modo(ModoInformacionDeSistema)
        elif codigo_tecla == 'F8':
            self._alternar_modo(ModoPuntosDeControl)
        elif codigo_tecla == 'F9':
            self._alternar_modo(ModoRadiosDeColision)
        elif codigo_tecla == 'F10':
            self._alternar_modo(ModoArea)
        elif codigo_tecla == 'F11':
            self._alternar_modo(ModoFisica)
        elif codigo_tecla == 'F12':
            self._alternar_modo(ModoPosicion)
        elif texto_tecla == '+':
            self._cambiar_grosor_de_bordes(+1)
        elif texto_tecla == '-':
            self._cambiar_grosor_de_bordes(-1)

    def cuando_mueve_el_mouse(self, x, y):
        self.posicion_del_mouse = x, y
        return True

    def _cambiar_grosor_de_bordes(self, cambio):
        ModoDepurador.grosor_de_lineas = min(max(1, ModoDepurador.grosor_de_lineas + cambio), 8)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = [x.__class__ for x in self.modos]

        if clase_del_modo in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)

    def _activar_modo(self, clase_del_modo):
        instancia_del_modo = clase_del_modo(self)
        self.modos.append(instancia_del_modo)
        self.modos.sort(key=lambda x: x.orden_de_tecla())

    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self.modos
                                if x.__class__ == clase_del_modo]
        self.modos.remove(instancia_a_eliminar[0])
        instancia_a_eliminar[0].sale_del_modo()

    def _mostrar_nombres_de_modos(self, painter):
        dy = 0
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        for modo in self.modos:
            texto = modo.tecla + " " + modo.__class__.__name__ + " habilitado."
            self.lienzo.texto_absoluto(painter, texto, izquierda + 10, arriba -20 +dy, color=pilas.colores.blanco)
            dy -= 20

    def _mostrar_posicion_del_mouse(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        x, y = self.posicion_del_mouse
        texto = u"Posición del mouse: x=%d y=%d " %(x, y)
        self.lienzo.texto_absoluto(painter, texto, derecha - 230, abajo + 10, color=pilas.colores.blanco)

    def _mostrar_cuadros_por_segundo(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        rendimiento = self.fps.obtener_cuadros_por_segundo()
        texto = "Cuadros por segundo: %s" %(rendimiento)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 10, color=pilas.colores.blanco)

    def _mostrar_cantidad_de_imagenes_cacheadas(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        total_de_imagenes_cacheadas = pilas.mundo.motor.libreria_imagenes.obtener_cantidad()
        texto = "Cantidad de imagenes cacheadas: %s" %(total_de_imagenes_cacheadas)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 70, color=pilas.colores.blanco)

    def _mostrar_cantidad_de_cuerpos(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        total_de_cuerpos = pilas.escena_actual().fisica.cantidad_de_cuerpos()
        texto = "Cantidad de cuerpos fisicos: %s" %(total_de_cuerpos)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 50, color=pilas.colores.blanco)

    def _mostrar_cantidad_de_actores(self, painter):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        total_de_actores = len(pilas.escena_actual().actores)
        texto = "Cantidad de actores: %s" %(total_de_actores)
        self.lienzo.texto_absoluto(painter, texto, izquierda + 10, abajo + 30, color=pilas.colores.blanco)

    def definir_modos(self, fisica=False, info=False, puntos_de_control=False,
                            radios=False, areas=False, posiciones=False, log=False):
        """Permite habilitar o deshabilitar los modos depuración.

        Cada uno de los argumentos representa un modo depuración, el valor True
        habilita el modo, False lo deshabilita.
        """
        self._desactivar_todos_los_modos()

        if log:
            self._alternar_modo(ModoWidgetLog)

        if info:
            self._alternar_modo(ModoInformacionDeSistema)

        if puntos_de_control:
            self._alternar_modo(ModoPuntosDeControl)

        if radios:
            self._alternar_modo(ModoRadiosDeColision)

        if areas:
            self._alternar_modo(ModoArea)

        if fisica:
            self._alternar_modo(ModoFisica)

        if posiciones:
            self._alternar_modo(ModoPosicion)


    def _desactivar_todos_los_modos(self):
        clases_activas = [x.__class__ for x in self.modos]

        for clase in clases_activas:
            self._desactivar_modo(clase)

    def reiniciar(self):
        self._desactivar_todos_los_modos()


class ModoDepurador(object):
    tecla = "F00"

    def __init__(self, depurador):
        self.depurador = depurador

    def comienza_dibujado(self, motor, painter, lienzo):
        pass

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        pass

    def termina_dibujado(self, motor, painter, lienzo):
        pass

    def orden_de_tecla(self):
        return int(self.tecla[1:])

    def sale_del_modo(self):
        pass

    def _obtener_posicion_relativa_a_camara(self, actor):
        if actor.fijo:
            return (actor.x, actor.y)
        else:
            return (actor.x - pilas.escena_actual().camara.x, actor.y - pilas.escena_actual().camara.y)

class ModoWidgetLog(ModoDepurador):
    tecla = "F5"

    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)
        self.widget = widget_log.WidgetLog()
        self.widget.show()
        self.widget.imprimir(locals())

    def sale_del_modo(self):
        self.widget.close()



class ModoInformacionDeSistema(ModoDepurador):
    tecla = "F7"

    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)

        self.informacion = [
            "Usando el motor: " + pilas.mundo.motor.nombre,
            "Sistema: " + sys.platform,
            "Version de pilas: " + pilasversion.VERSION,
            "Version de python: " + sys.subversion[0] + " " + sys.subversion[1],
            "Version de Box2D: {}".format(pilas.fisica.obtener_version()),
            ]

    def termina_dibujado(self, motor, painter, lienzo):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        for (i, texto) in enumerate(self.informacion):
            posicion_y = abajo + 90 + i * 20
            lienzo.texto(painter, texto, izquierda + 10, posicion_y, color=pilas.colores.blanco)


class ModoPuntosDeControl(ModoDepurador):
    tecla = "F8"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        x, y = self._obtener_posicion_relativa_a_camara(actor)
        lienzo.cruz(painter, x, y, color=pilas.colores.negro, grosor=ModoDepurador.grosor_de_lineas+2)
        lienzo.cruz(painter, x, y, color=pilas.colores.blanco, grosor=ModoDepurador.grosor_de_lineas)


class ModoRadiosDeColision(ModoDepurador):
    tecla = "F9"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        x, y = self._obtener_posicion_relativa_a_camara(actor)
        lienzo.circulo(painter, x, y, actor.radio_de_colision, color=pilas.colores.negro, grosor=ModoDepurador.grosor_de_lineas+2)
        lienzo.circulo(painter, x, y, actor.radio_de_colision, color=pilas.colores.blanco, grosor=ModoDepurador.grosor_de_lineas)


class ModoArea(ModoDepurador):
    tecla = "F10"

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        dx, dy = actor.centro
        x, y = self._obtener_posicion_relativa_a_camara(actor)
        lienzo.rectangulo(painter, x - dx, y + dy, actor.ancho, actor.alto, color=pilas.colores.negro, grosor=ModoDepurador.grosor_de_lineas+2)
        lienzo.rectangulo(painter, x - dx, y + dy, actor.ancho, actor.alto, color=pilas.colores.blanco, grosor=ModoDepurador.grosor_de_lineas)


class ModoFisica(ModoDepurador):
    tecla = "F11"

    def termina_dibujado(self, motor, painter, lienzo):
        grosor = ModoDepurador.grosor_de_lineas
        pilas.escena_actual().fisica.dibujar_figuras_sobre_lienzo(painter, lienzo, grosor)


class ModoPosicion(ModoDepurador):
    tecla = "F12"

    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)
        self.eje = pilas.actores.Ejes()

    def dibuja_al_actor(self, motor, painter, lienzo, actor):
        if not isinstance(actor, pilas.fondos.Fondo):
            texto = "(%d, %d)" %(actor.x, actor.y)
            dx, dy = 30, - 30
            x, y = self._obtener_posicion_relativa_a_camara(actor)
            lienzo.texto(painter, texto, x + dx, y + dy, color=pilas.colores.blanco)

    def sale_del_modo(self):
        self.eje.eliminar()
