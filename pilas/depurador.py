# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class Depurador:
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
        self.fps = fps
        self.posicion_del_mouse = (0, 0)
        pilas.eventos.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
        
    def cuando_mueve_el_mouse(self, evento):
        self.posicion_del_mouse = (evento.x, evento.y)
        return True

    def comienza_dibujado(self, motor):
        for m in self.modos:
            m.comienza_dibujado(motor, self.lienzo)

    def dibuja_al_actor(self, motor, actor):
        for m in self.modos:
            m.dibuja_al_actor(motor, self.lienzo, actor)

    def termina_dibujado(self, motor):
        if self.modos:
            self._mostrar_cuadros_por_segundo(motor)
            self._mostrar_posicion_del_mouse(motor)
            self._mostrar_nombres_de_modos(motor)

            for m in self.modos:
                m.termina_dibujado(motor, self.lienzo)
    
    def cuando_pulsa_tecla(self, evento):
        if evento.codigo == 'F8':
            self._alternar_modo(ModoPuntosDeControl)
        elif evento.codigo == 'F9':
            self._alternar_modo(ModoRadiosDeColision)
        elif evento.codigo == 'F10':
            self._alternar_modo(ModoArea)
        elif evento.codigo == 'F11':
            self._alternar_modo(ModoFisica)
        elif evento.codigo == 'F12':
            self._alternar_modo(ModoPosicion)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = [x.__class__ for x in self.modos]
        
        if clase_del_modo in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)
    
    def _activar_modo(self, clase_del_modo):
        pilas.eventos.inicia_modo_depuracion.send('depurador')
        instancia_del_modo = clase_del_modo(self)
        self.modos.append(instancia_del_modo)
        # Ordena todos los registros por numero de tecla.
        self.modos.sort(key=lambda x: x.orden_de_tecla())
        
    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self.modos 
                                if x.__class__ == clase_del_modo]
        self.modos.remove(instancia_a_eliminar[0])
        
        if not self.modos:
            pilas.eventos.sale_modo_depuracion.send('depurador')

    def _mostrar_nombres_de_modos(self, motor):
        dy = 0
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()

        for modo in self.modos:
            texto = modo.tecla + " " + modo.__class__.__name__ + " habilitado."
            self.lienzo.texto_absoluto(motor, texto, izquierda + 10, arriba -20 +dy, 
                    color=pilas.colores.violeta)
            dy -= 20
            
    def _mostrar_posicion_del_mouse(self, motor):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        x, y = self.posicion_del_mouse    
        texto = u"Posición del mouse: x=%d y=%d " %(x, y)
        self.lienzo.texto_absoluto(motor, texto, derecha - 230, abajo + 10, color=pilas.colores.violeta)
        
    def _mostrar_cuadros_por_segundo(self, motor):
        izquierda, derecha, arriba, abajo = pilas.utils.obtener_bordes()
        rendimiento = self.fps.obtener_cuadros_por_segundo()
        texto = "Cuadros por segundo: %s" %(rendimiento)
        self.lienzo.texto_absoluto(motor, texto, izquierda + 10, abajo + 10, 
                color=pilas.colores.violeta)
        
class ModoDepurador:
    tecla = "F00"

    def __init__(self, depurador):
        self.depurador = depurador
        
    def comienza_dibujado(self, motor, lienzo):
        pass
    
    def dibuja_al_actor(self, motor, lienzo, actor):
        pass

    def termina_dibujado(self, motor, lienzo):
        pass
     
    def orden_de_tecla(self):
        return int(self.tecla[1:])
    
class ModoPuntosDeControl(ModoDepurador):
    tecla = "F8"
    
    def dibuja_al_actor(self, motor, lienzo, actor):
        lienzo.cruz(motor, actor.x, actor.y, color=pilas.colores.rojo)
        
class ModoRadiosDeColision(ModoDepurador):
    tecla = "F9"
    
    def dibuja_al_actor(self, motor, lienzo, actor):
        lienzo.circulo(motor, actor.x, actor.y, actor.radio_de_colision, color=pilas.colores.verde)
 
class ModoArea(ModoDepurador):
    tecla = "F10"
    
    def dibuja_al_actor(self, motor, lienzo, actor):
        dx, dy = actor.centro
        lienzo.rectangulo(motor, actor.x - dx, actor.y + dy, actor.ancho, actor.alto, color=pilas.colores.azul)

class ModoPosicion(ModoDepurador):
    tecla = "F12"
    
    def __init__(self, depurador):
        ModoDepurador.__init__(self, depurador)

    def dibuja_al_actor(self, motor, lienzo, actor):
        texto = "(%d, %d)" %(actor.x, actor.y)
        lienzo.texto(motor, texto, actor.x, actor.y, color=pilas.colores.violeta)
        
class ModoFisica(ModoDepurador):
    tecla = "F11"
    
    def termina_dibujado(self, motor, lienzo):
        pilas.mundo.fisica.dibujar_figuras_sobre_lienzo(motor, lienzo)
