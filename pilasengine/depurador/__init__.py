# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo_info import ModoInformacionDeSistema

class Depurador(object):

    def __init__(self, pilas):
        self.pilas = pilas
        self._modos = []

    def obtener_modos_habilitados(self):
        """Retorna una lista con los nombres de los modos habilitados."""
        modos = [x.__class__.__name__ for x in self._modos]
        return modos

    def definir_modos(self, info=False, radios=False, posiciones=False,
                      puntos_de_control=False, areas=False,
                      fisica=False):
        """Permite habilitar o deshabilitar los modos depuración.

        Cada uno de los argumentos representa un modo depuración, el valor True
        habilita el modo, False lo deshabilita.
        """
        modos = self.obtener_modos_habilitados()

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

    def _alternar_modo(self, clase_del_modo):
        clases_activas = self.obtener_modos_habilitados()

        if clase_del_modo.__name__ in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)

    def _activar_modo(self, clase_del_modo):
        instancia_del_modo = clase_del_modo(self.pilas, self)
        self._modos.append(instancia_del_modo)
        self._modos.sort(key=lambda x: x.orden_de_tecla())

    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self._modos
                                if x.__class__ == clase_del_modo]
        self._modos.remove(instancia_a_eliminar[0])
        instancia_a_eliminar[0].sale_del_modo()